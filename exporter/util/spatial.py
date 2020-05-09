import logging

from gtfslib.model import Trip, Shape
from gtfslib.spatial import orthodromic_distance, orthodromic_seg_distance, DistanceCache
from gtfslib.utils import ContinousPiecewiseLinearFunc

logger = logging.getLogger("gtfsexporter")


class _CacheEntry(object):

    def __init__(self, distance):
        self._distance = distance
        self._next_entries = {}

    def next_entry(self, stop):
        return self._next_entries.get(stop.stop_id)

    def distance(self):
        return self._distance

    def insert(self, stop, distance):
        next_entry = _CacheEntry(distance)
        self._next_entries[stop.stop_id] = next_entry
        return next_entry


class _OdometerShape(object):
    # A 0.1% cone - Coefficient to defavor points further away on a shape
    # when doing stop snapping to shape. The summit angle of the offset cone
    # is 2 * arctan(K).
    K = 0.001

    def __init__(self, shape):
        self._shape = shape
        self._cache = _CacheEntry(None)
        self._cache_hit = 0
        self._cache_miss = 0
        if all(pt.shape_dist_traveled != -999999 for pt in shape.points):
            self._xdist = ContinousPiecewiseLinearFunc()
        else:
            self._xdist = None
        # Normalize the shape here:
        # 1) dist_traveled to meters
        # 2) pt_seq to contiguous numbering from 0
        ptseq = 0
        distance_meters = 0.0
        last_pt = None
        shape.points.sort(key=lambda p: p.shape_pt_sequence)
        for pt in shape.points:
            if last_pt is not None:
                # Note: we do not use distance cache, as most probably
                # many of the points will be different from each other.
                distance_meters += orthodromic_distance(last_pt, pt)
            last_pt = pt
            pt.shape_pt_sequence = ptseq
            old_distance = pt.shape_dist_traveled
            pt.shape_dist_traveled = distance_meters
            # Remember the distance mapping for stop times
            if self._xdist:
                self._xdist.append(old_distance, pt.shape_dist_traveled)
            ptseq += 1

    def reset(self):
        self._distance = 0
        self._istart = 0
        self._cache_cursor = self._cache

    def dist_traveled(self, stop, old_dist_traveled):
        if old_dist_traveled and self._xdist:
            # Case 1: we have in the original data shape_dist_traveled
            # We need to remap from the old scale to the new meter scale
            return self._xdist.interpolate(old_dist_traveled)
        else:
            # Case 2: we do not have original shape_dist_traveled
            # We need to determine ourselves where in the shape we lie
            # TODO Implement a cache, this can be slow for lots of trips
            # and the result is the same for the same pattern
            # Check the cache first
            cache_entry = self._cache_cursor.next_entry(stop)
            if cache_entry is not None:
                self._cache_cursor = cache_entry
                self._cache_hit += 1
                return cache_entry.distance()
            min_dist = 1e20
            best_i = self._istart
            best_dist = 0
            for i in range(self._istart, len(self._shape.points) - 1):
                a = self._shape.points[i]
                b = self._shape.points[i + 1]
                dist, pdist = orthodromic_seg_distance(stop, a, b)
                newdist = a.shape_dist_traveled + pdist
                howfar = newdist - self._distance
                # Add a slight "cone" offset. There are pathological
                # cases with backtracking shapes where the best distance
                # is slightly better way further (for eg 0.01m) than at
                # the starting point (for eg 0.02m). In that case we should
                # obviously keep the first point instead of moving too fast
                # to the shape end. That offset should help for some cases.
                dist += howfar * self.K
                if dist < min_dist:
                    min_dist = dist
                    best_i = i
                    best_dist = newdist
            if best_dist > self._distance:
                self._distance = best_dist
            else:
                delta = self._distance - best_dist
                if delta > 10:
                    # This is harmless if the backtracking distance is small.
                    # We have lots of false positive (<<1m) due to rounding errors.
                    logger.warn(
                        "Backtracking of %f m detected in shape %s for stop %s (%s) (%f,%f) at distance %f < %f m on segment #[%d-%d]" % (
                            delta, self._shape.shape_id, stop.stop_id, stop.stop_name, stop.stop_lat, stop.stop_lon,
                            best_dist, self._distance, best_i, best_i + 1))
            self._istart = best_i
            self._cache_miss += 1
            self._cache_cursor = self._cache_cursor.insert(stop, self._distance)
            return self._distance

    def _debug_cache(self):
        logger.debug("Shape %s: Cache hit: %d, misses: %d" % (self._shape.shape_id, self._cache_hit, self._cache_miss))


class _Odometer(object):
    _odoshp = None
    _dcache = None

    def normalize_and_register_shape(self, shape):
        self._odoshp = _OdometerShape(shape)
        self.reset()

    def register_noshape(self):
        self._odoshp = None
        self.reset()

    def reset(self):
        if self._odoshp is not None:
            self._odoshp.reset()
        self._distance = 0
        self._last_stop = None
        self._dcache = DistanceCache()

    def dist_traveled(self, stop, old_dist_traveled):
        if self._odoshp is not None:
            # We have a shape, use it
            return self._odoshp.dist_traveled(stop, old_dist_traveled)
        # We do not have shape, use straight-line distance between
        # consecutive stops
        if self._last_stop is not None:
            self._distance += self._dcache.orthodromic_distance(self._last_stop, stop)
        self._last_stop = stop
        return self._distance

    def _debug_cache(self):
        self._odoshp._debug_cache()


def normalize_trip(trip, odometer):
    stopseq = 0
    n_stoptimes = len(trip.stop_times)
    last_stoptime_with_time = None
    to_interpolate = []
    odometer.reset()
    for stoptime in trip.stop_times:
        stoptime.stop_sequence = stopseq
        stoptime.shape_dist_traveled = odometer.dist_traveled(stoptime.stop,
                                                              stoptime.shape_dist_traveled if stoptime.shape_dist_traveled != -999999 else None)
        if stopseq == 0:
            # Force first arrival time to NULL
            stoptime.arrival_time = None
        if stopseq == n_stoptimes - 1:
            # Force last departure time to NULL
            stoptime.departure_time = None
        if stoptime.interpolated:
            to_interpolate.append(stoptime)
        else:
            if len(to_interpolate) > 0:
                # Interpolate
                if last_stoptime_with_time is None:
                    logger.error("Cannot interpolate missing time at trip start: %s" % trip)
                    for stti in to_interpolate:
                        # Use first defined time as fallback value.
                        stti.arrival_time = stoptime.arrival_time
                        stti.departure_time = stoptime.arrival_time
                else:
                    tdist = stoptime.shape_dist_traveled - last_stoptime_with_time.shape_dist_traveled
                    ttime = stoptime.arrival_time - last_stoptime_with_time.departure_time
                    for stti in to_interpolate:
                        fdist = stti.shape_dist_traveled - last_stoptime_with_time.shape_dist_traveled
                        t = last_stoptime_with_time.departure_time + ttime * fdist // tdist
                        stti.arrival_time = t
                        stti.departure_time = t
            to_interpolate = []
            last_stoptime_with_time = stoptime
        stopseq += 1
    if len(to_interpolate) > 0:
        # Should not happen, but handle the case, we never know
        if last_stoptime_with_time is None:
            logger.error("Cannot interpolate missing time, no time at all: %s" % trip)
            # Keep times NULL (TODO: or remove the trip?)
        else:
            logger.error("Cannot interpolate missing time at trip end: %s" % trip)
            for stti in to_interpolate:
                # Use last defined time as fallback value
                stti.arrival_time = last_stoptime_with_time.departure_time
                stti.departure_time = last_stoptime_with_time.departure_time


class DataNormalizer:
    def __init__(self, dao, feed_id):
        self.__dao = dao
        self.__feed_id = feed_id

    def normalize(self):
        logger.info("Normalizing shapes and trips...")
        nshapes = 0
        ntrips = 0
        odometer = _Odometer()
        # Process shapes and associated trips
        for shape in self.__dao.shapes(fltr=Shape.feed_id == self.__feed_id, prefetch_points=True, batch_size=50):
            # Shape will be registered in the normalize
            odometer.normalize_and_register_shape(shape)
            for trip in self.__dao.trips(fltr=(Trip.feed_id == self.__feed_id) & (Trip.shape_id == shape.shape_id),
                                         prefetch_stop_times=True, prefetch_stops=True, batch_size=800):
                normalize_trip(trip, odometer)
                ntrips += 1
                if ntrips % 1000 == 0:
                    logger.info("%d trips, %d shapes" % (ntrips, nshapes))
                    self.__dao.flush()
            nshapes += 1
            # odometer._debug_cache()
        # Process trips w/o shapes
        for trip in self.__dao.trips(fltr=(Trip.feed_id == self.__feed_id) & (Trip.shape_id == None),
                                     prefetch_stop_times=True,
                                     prefetch_stops=True, batch_size=800):
            odometer.register_noshape()
            normalize_trip(trip, odometer)
            ntrips += 1
            if ntrips % 1000 == 0:
                logger.info("%d trips" % ntrips)
                self.__dao.flush()
        self.__dao.flush()
        logger.info("Normalized %d trips and %d shapes" % (ntrips, nshapes))
