import logging
import os
import zipfile

import io
import six
import csv

from exporter.gtfs.model import Stop, Transfer, FareAttribute, FareRule
from exporter.gtfs.utils import fmttime, group_pairs

logger = logging.getLogger("gtfsexporter")

class PrettyCsv(object):
    """Act as a csv DictWriter or console pretty-printer, according to whether outfile is set or not."""

    def __init__(self, outfile, fieldnames=None, maxwidth=120, **kwargs):
        self._fieldnames = fieldnames
        if outfile:
            self._rows = None
            if not outfile.endswith('.csv') and not outfile.endswith('.txt'):
                outfile += '.csv'
            if six.PY2:
                self._csvfile = open(outfile, 'wb')
            else:
                self._csvfile = io.TextIOWrapper(open(outfile, 'wb'), encoding='utf-8')
            self._csv = csv.writer(self._csvfile, **kwargs)
            if self._fieldnames is not None:
                # Write header
                self._csv.writerow(self._fieldnames)
        else:
            self._maxwidth = int(maxwidth)
            self._csv = None
            self._rows = []

    def writerow(self, row):
        if isinstance(row, dict):
            if self._fieldnames is None:
                raise Exception("You can't add a row as dictionnary w/o specifying fieldnames!")
            row = [ row.get(fieldname, None) for fieldname in self._fieldnames ]
        # Force to unicode
        row = [ six.u("") if v is None else v if isinstance(v, six.text_type) else six.u(str(v)) for v in row ]
        if self._csv:
            if six.PY2:
                self._csv.writerow([ v.encode('utf-8') for v in row ])
            else:
                self._csv.writerow(row)
        if self._rows is not None:
            self._rows.append(row)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._csv:
            self._csvfile.close()
        else:
            if self._fieldnames is not None:
                allrows = [ self._fieldnames ] + self._rows
            else:
                allrows = self._rows
            ncols = max(len(row) for row in allrows)
            colwidths = [ 0 for i in range(0, ncols) ]
            for row in allrows:
                for i in range(0, len(row)):
                    cell = row[i]
                    l = min(self._maxwidth, len(cell))
                    if cell and l > colwidths[i]:
                        colwidths[i] = l
            if self._fieldnames is not None:
                self._prettysep(colwidths)
                self._prettyprint(colwidths, self._fieldnames)
            self._prettysep(colwidths)
            for row in self._rows:
                self._prettyprint(colwidths, row)
            self._prettysep(colwidths)

    def _prettyprint(self, widths, row):
        s = "|"
        for width, cell in six.moves.zip_longest(widths, row, fillvalue=None):
            scell = six.u("") if cell is None else cell
            diff = width - len(scell)
            s += ' ' + (' ' * diff) + scell[:width] + ' |'
        print(s)

    def _prettysep(self, widths):
        s = "+"
        for width in widths:
            s += '-' * (width + 1) + '-+'
        print(s)

class Context(object):
    """The class given as execution context to a plugin.
    Propose helper methods to filter objects, or get the DAO."""

    def __init__(self, dao, args, out_path):
        self._dao = dao
        self.args = args
        self._out_path = out_path

    @property
    def dao(self):
        return self._dao

    @property
    def out_path(self):
        return self._out_path

class Writer(object):
    """
    Export some data in GTFS-compatible format.

    Parameters:
    --skip_shape_dist     To remove shape_dist_traveled from the export.
    --bundle[=<zipfile>]  Zip the result (using filename if given,
                          otherwise default to "gtfs.zip").

    Examples:
    --filter="(Route.route_short_name=='R1')"
      Restrict to route R1
    """

    def __init__(self, context: Context, skip_shape_dist=False, bundle=None, **kwargs):
        self.context = context
        self.skip_shape_dist = skip_shape_dist
        self.bundle = bundle

    def run(self, **kwargs):
        with PrettyCsv(os.path.join(self.context.out_path,"agency.txt"),
                       ["agency_id", "agency_name", "agency_url", "agency_timezone", "agency_lang", "agency_phone",
                        "agency_fare_url", "agency_email"], **kwargs) as csvout:
            nagencies = 0
            for agency in self.context.dao.agencies(fltr=self.context.args.filter):
                nagencies += 1
                csvout.writerow([agency.agency_id, agency.agency_name, agency.agency_url, agency.agency_timezone,
                                 agency.agency_lang, agency.agency_phone, agency.agency_fare_url, agency.agency_email])
            logger.info("Exported %d agencies" % (nagencies))

        stop_ids = set()
        zone_ids = set()

        def _output_stop(stop):
            csvout.writerow([stop.stop_id, stop.stop_code, stop.stop_name, stop.stop_desc, stop.stop_lat, stop.stop_lon,
                             stop.zone_id, stop.stop_url, stop.location_type, stop.parent_station_id,
                             stop.stop_timezone, stop.wheelchair_boarding])

        with PrettyCsv(os.path.join(self.context.out_path,"stops.txt"),
                       ["stop_id", "stop_code", "stop_name", "stop_desc", "stop_lat", "stop_lon", "zone_id", "stop_url",
                        "location_type", "parent_station", "stop_timezone", "wheelchair_boarding"], **kwargs) as csvout:
            nstops = 0
            station_ids = set()
            for stop in self.context.dao.stops(fltr=self.context.args.filter, prefetch_parent=False,
                                                 prefetch_substops=False):
                _output_stop(stop)
                stop_ids.add((stop.feed_id, stop.stop_id))
                if stop.parent_station_id is not None:
                    station_ids.add((stop.feed_id, stop.parent_station_id))
                if stop.zone_id is not None:
                    zone_ids.add((stop.feed_id, stop.zone_id))
                nstops += 1
            # Only export parent station that have not been already seen
            station_ids -= stop_ids
            for feed_id, st_ids in group_pairs(station_ids, 1000):
                for station in self.context.dao.stops(fltr=(Stop.feed_id == feed_id) & (Stop.stop_id.in_(st_ids))):
                    _output_stop(station)
                    if station.zone_id is not None:
                        zone_ids.add((station.feed_id, station.zone_id))
                    nstops += 1
            logger.info("Exported %d stops" % (nstops))
            stop_ids |= station_ids

        route_ids = set()
        with PrettyCsv(os.path.join(self.context.out_path,"routes.txt"),
                       ["route_id", "agency_id", "route_short_name", "route_long_name", "route_desc", "route_type",
                        "route_url", "route_color", "route_text_color"], **kwargs) as csvout:
            nroutes = 0
            for route in self.context.dao.routes(fltr=self.context.args.filter):
                nroutes += 1
                csvout.writerow(
                    [route.route_id, route.agency_id, route.route_short_name, route.route_long_name, route.route_desc,
                     route.route_type, route.route_url, route.route_color, route.route_text_color])
                route_ids.add((route.feed_id, route.route_id))
            logger.info("Exported %d routes" % (nroutes))

        stop_times_columns = ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence", "stop_headsign",
                              "pickup_type", "drop_off_type", "timepoint"]
        if not self.skip_shape_dist:
            stop_times_columns.append("shape_dist_traveled")
        with PrettyCsv(os.path.join(self.context.out_path,"trips.txt"),
                       ["route_id", "service_id", "trip_id", "trip_headsign", "trip_short_name", "direction_id",
                        "block_id", "shape_id", "wheelchair_accessible", "bikes_allowed"], **kwargs) as csvout1:
            with PrettyCsv(os.path.join(self.context.out_path,"stop_times.txt"), stop_times_columns, **kwargs) as csvout2:
                ntrips = 0
                nstoptimes = 0
                for trip in self.context.dao.trips(fltr=self.context.args.filter, prefetch_stops=False,
                                                     prefetch_stop_times=True, prefetch_calendars=False,
                                                     prefetch_routes=False):
                    ntrips += 1
                    if ntrips % 1000 == 0:
                        logger.info("%d trips..." % (ntrips))
                    csvout1.writerow(
                        [trip.route_id, trip.service_id, trip.trip_id, trip.trip_headsign, trip.trip_short_name,
                         trip.direction_id, trip.block_id, trip.shape_id, trip.wheelchair_accessible,
                         trip.bikes_allowed])
                    for stoptime in trip.stop_times:
                        nstoptimes += 1
                        row = [trip.trip_id,
                               fmttime(
                                   stoptime.arrival_time if stoptime.arrival_time is not None else stoptime.departure_time),
                               fmttime(
                                   stoptime.departure_time if stoptime.departure_time is not None else stoptime.arrival_time),
                               stoptime.stop_id,
                               stoptime.stop_sequence,
                               stoptime.stop_headsign,
                               stoptime.pickup_type,
                               stoptime.drop_off_type,
                               stoptime.timepoint if (stoptime.arrival_time is not None or stoptime.departure_time is not None) else 0]
                        if not self.skip_shape_dist:
                            row.append(stoptime.shape_dist_traveled)
                        csvout2.writerow(row)
                logger.info("Exported %d trips with %d stop times" % (ntrips, nstoptimes))

        # Note: GTFS' model does not have calendars objects to export,
        # since a calendar is renormalized/expanded to a list of dates.

        with PrettyCsv(os.path.join(self.context.out_path,"calendar_dates.txt"), ["service_id", "date", "exception_type"], **kwargs) as csvout:
            ncals = ndates = 0
            for calendar in self.context.dao.calendars(fltr=self.context.args.filter, prefetch_dates=True):
                ncals += 1
                if ncals % 1000 == 0:
                    logger.info("%d calendars, %d dates..." % (ncals, ndates))
                for date in calendar.dates:
                    ndates += 1
                    csvout.writerow([calendar.service_id, date.toYYYYMMDD(), 1])
            logger.info("Exported %d calendars with %d dates" % (ncals, ndates))

        fare_attr_ids = set()
        nfarerules = [0]

        def _output_farerule(farerule):
            if farerule.route_id is not None and (farerule.feed_id, farerule.route_id) not in route_ids:
                return False
            if farerule.origin_id is not None and (farerule.feed_id, farerule.origin_id) not in zone_ids:
                return False
            if farerule.contains_id is not None and (farerule.feed_id, farerule.contains_id) not in zone_ids:
                return False
            if farerule.destination_id is not None and (farerule.feed_id, farerule.destination_id) not in zone_ids:
                return False
            csvout.writerow([farerule.fare_id, farerule.route_id, farerule.origin_id, farerule.destination_id,
                             farerule.contains_id])
            fare_attr_ids.add((farerule.feed_id, farerule.fare_id))
            nfarerules[0] += 1
            return True

        with PrettyCsv(os.path.join(self.context.out_path,"fare_rules.txt"), ["fare_id", "route_id", "origin_id", "destination_id", "contains_id"],
                       **kwargs) as csvout:
            feed_ids = set()
            for feed_id, rt_ids in group_pairs(route_ids, 1000):
                feed_ids.add(feed_id)
                for farerule in self.context.dao.fare_rules(
                        fltr=(FareRule.feed_id == feed_id) & FareRule.route_id.in_(rt_ids),
                        prefetch_fare_attributes=False):
                    if not _output_farerule(farerule):
                        continue
            for feed_id, zn_ids in group_pairs(zone_ids, 1000):
                feed_ids.add(feed_id)
                for farerule in self.context.dao.fare_rules(fltr=(FareRule.feed_id == feed_id) & (
                        FareRule.origin_id.in_(zn_ids) | FareRule.contains_id.in_(zn_ids) | FareRule.destination_id.in_(
                        zn_ids)), prefetch_fare_attributes=False):
                    if not _output_farerule(farerule):
                        continue
            # Special code to include all fare rules w/o any relationships
            # of any feed_id we've encountered so far
            for feed_id in feed_ids:
                for farerule in self.context.dao.fare_rules(
                        fltr=(FareRule.feed_id == feed_id) & (FareRule.route_id == None) & (
                                FareRule.origin_id == None) & (FareRule.contains_id == None) & (
                                     FareRule.destination_id == None), prefetch_fare_attributes=False):
                    if not _output_farerule(farerule):
                        continue
            logger.info("Exported %d fare rules" % (nfarerules[0]))
        if nfarerules[0] == 0:
            os.remove(os.path.join(self.context.out_path,"fare_rules.txt"))

        with PrettyCsv(os.path.join(self.context.out_path,"fare_attributes.txt"),
                       ["fare_id", "price", "currency_type", "payment_method", "transfers", "transfer_duration"],
                       **kwargs) as csvout:
            nfareattrs = 0
            for feed_id, fa_ids in group_pairs(fare_attr_ids, 1000):
                for fareattr in self.context.dao.fare_attributes(
                        fltr=(FareAttribute.feed_id == feed_id) & FareAttribute.fare_id.in_(fa_ids),
                        prefetch_fare_rules=False):
                    nfareattrs += 1
                    csvout.writerow([fareattr.fare_id, fareattr.price, fareattr.currency_type, fareattr.payment_method,
                                     fareattr.transfers, fareattr.transfer_duration])
            logger.info("Exported %d fare attributes" % (nfareattrs))
        if nfareattrs == 0:
            os.remove(os.path.join(self.context.out_path,"fare_attributes.txt"))

        shapes_columns = ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]
        if not self.skip_shape_dist:
            shapes_columns.append("shape_dist_traveled")
        with PrettyCsv(os.path.join(self.context.out_path, "shapes.txt"), shapes_columns, **kwargs) as csvout:
            nshapes = nshapepoints = 0
            for shape in self.context.dao.shapes(fltr=self.context.args.filter, prefetch_points=True):
                nshapes += 1
                if nshapes % 100 == 0:
                    logger.info("%d shapes, %d points..." % (nshapes, nshapepoints))
                for point in shape.points:
                    nshapepoints += 1
                    row = [shape.shape_id, point.shape_pt_lat, point.shape_pt_lon, point.shape_pt_sequence]
                    if not self.skip_shape_dist:
                        row.append(point.shape_dist_traveled)
                    csvout.writerow(row)
            logger.info("Exported %d shapes with %d points" % (nshapes, nshapepoints))
        if nshapes == 0:
            os.remove(os.path.join(self.context.out_path,"shapes.txt"))

        with PrettyCsv(os.path.join(self.context.out_path,"transfers.txt"), ["from_stop_id", "to_stop_id", "transfer_type", "min_transfer_time"],
                       **kwargs) as csvout:
            ntransfers = 0
            transfer_ids = set()
            for feed_id, st_ids in group_pairs(stop_ids, 1000):
                # Note: we can't use a & operator below instead of |,
                # as we would need to have *all* IDs in one batch.
                for transfer in self.context.dao.transfers(fltr=(Transfer.feed_id == feed_id) & (
                        Transfer.from_stop_id.in_(st_ids) | Transfer.to_stop_id.in_(st_ids)), prefetch_stops=False):
                    # As we used from_stop_id.in(...) OR to_stop_id.in(...),
                    # we need to filter out the potential superfluous results.
                    from_stop_id = (transfer.feed_id, transfer.from_stop_id)
                    to_stop_id = (transfer.feed_id, transfer.to_stop_id)
                    if from_stop_id not in stop_ids or to_stop_id not in stop_ids:
                        continue
                    transfer_id = (from_stop_id, to_stop_id)
                    if transfer_id in transfer_ids:
                        # Prevent duplicates (can happen from grouping)
                        continue
                    transfer_ids.add(transfer_id)
                    ntransfers += 1
                    csvout.writerow([transfer.from_stop_id, transfer.to_stop_id, transfer.transfer_type,
                                     transfer.min_transfer_time])
            logger.info("Exported %d transfers" % (ntransfers))
        if ntransfers == 0:
            os.remove(os.path.join(self.context.out_path,"transfers.txt"))

        if self.bundle:
            from exporter.util.storage import generate_gtfs_bundle
            generate_gtfs_bundle(self.context.out_path, bundle=self.bundle)