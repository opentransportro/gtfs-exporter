import logging
import os

from exporter.gtfs.dao import Dao
from exporter.util.perf import run_command, check_utility
from exporter import __map_path__
from exporter.util.storage import file_age_in_seconds

from exporter.util.http import Request

logger = logging.getLogger("gtfsexporter")


class Processor:
    def process(self, dao: Dao):
        pass


class RouteColorProcessor(Processor):
    def process(self, dao: Dao):
        for route in dao.routes():
            logger.info("updating route [%s] setting correct color" % route.route_long_name)

            route.route_text_color = "FFFFFF"

            from exporter.gtfs.model import Route
            if route.route_type == Route.TYPE_BUS:
                route.route_color = "195BAD"
            elif route.route_type == Route.TYPE_TRAM:
                route.route_color = "FFAD33"
            elif route.route_type == Route.TYPE_RAIL:
                route.route_color = "FF5B33"
            elif route.route_type == Route.TYPE_CABLECAR:
                route.route_color = "FF8433"
            elif route.route_type == Route.TYPE_SUBWAY:
                route.route_color = "D13333"
            elif route.route_type == Route.TYPE_FERRY:
                route.route_color = "62A9DD"

        dao.commit()


class OSRMTimeProcessor(Processor):
    def __init__(self):
        logger.info("Checking if downloading maps is required.")
        self.download_file(["map.osrm",
                            "map.osrm.ramIndex",
                            "map.osrm.fileIndex",
                            "map.osrm.edges",
                            "map.osrm.geometry",
                            "map.osrm.turn_weight_penalties",
                            "map.osrm.turn_duration_penalties",
                            "map.osrm.cnbg_to_ebg",
                            "map.osrm.datasource_names",
                            "map.osrm.names",
                            "map.osrm.timestamp",
                            "map.osrm.properties",
                            "map.osrm.icd",
                            "map.osrm.maneuver_overrides",
                            "map.osrm.nbg_nodes",
                            "map.osrm.ebg_nodes",
                            "map.osrm.tls",
                            "map.osrm.tld",
                            "map.osrm.restrictions",
                            "map.osrm.partition",
                            "map.osrm.mldgr",
                            "map.osrm.enw",
                            "map.osrm.ebg",
                            "map.osrm.cnbg",
                            "map.osrm.cell_metrics",
                            "map.osrm.cells"])

        check_utility("docker")

        # start docker
        # client = docker.from_env()
        # client.containers.run(image="osrm/osrm-backend", command="osrm-routed --algorithm mld /data/map.osrm",
        #                       ports={"5000":"5000"}, volumes={f"{__map_path__}":"/data"}, detach=False, )
        run_command(["docker", "run", "--rm", "--name", "osrm", "-d",
                     "-p", "5000:5000",
                     "-v", f"{__map_path__}:/data",
                     "osrm/osrm-backend",
                     "osrm-routed", "--algorithm=MLD", "/data/map.osrm"
                     ])

    @staticmethod
    def download_file(file_names: list):
        for file_name in file_names:
            downloaded_file = os.path.join(__map_path__, file_name)

            if not os.path.exists(downloaded_file) or file_age_in_seconds(downloaded_file) > 604800:
                if os.path.exists(downloaded_file) and file_age_in_seconds(downloaded_file) > 604800:
                    logger.warning("Map file to old removing and fetching new one!")
                    os.remove(downloaded_file)

                if not os.path.exists(downloaded_file):
                    logger.info(
                        f"downloading from https://github.com/opentransportro/osrm-maps/releases/download/latest/{file_name}")
                    import requests
                    file = requests.get(
                        f"https://github.com/opentransportro/osrm-maps/releases/download/latest/{file_name}",
                        stream=True)

                    with open(downloaded_file, "wb") as exported_file:
                        total_length = int(file.headers.get('content-length'))
                        from clint.textui import progress
                        for ch in progress.bar(file.iter_content(chunk_size=2391975),
                                               expected_size=(total_length / 1024) + 1):
                            if ch:
                                exported_file.write(ch)

    def __del__(self):
        # stop docker
        run_command(["docker", "stop", "osrm"])

    def process(self, dao: Dao):
        for route in dao.routes():
            # use the first trip as time template to improve overall performance
            if len(route.trips) > 0:
                self.__process_trips_per_direction(route, 0)
                self.__process_trips_per_direction(route, 1)
                
        dao.commit()

    def __process_trips_per_direction(self, route, direction_id):
        trip_template = next(trip for trip in route.trips if trip.direction_id == direction_id)
        trip_template_coords = []
        trip_template_times = []

        for idx, stop_time in enumerate(trip_template.stop_times, start=0):
            trip_template_coords.append([stop_time.stop.stop_lon, stop_time.stop.stop_lat])
            if idx == 0:
                trip_template_times.append(0)    
            else:
                trip_template_times.append(self.__compute_osrm_time(trip_template_coords))

        for trip in filter(lambda trip: trip.direction_id == direction_id, route.trips):
            for idx, stop_time in enumerate(trip.stop_times, start=0):
                if idx == 0:
                    pass
                else:
                    stop_time.departure_time = trip_template_times[idx] + trip.stop_times[0].departure_time


    def __compute_osrm_time(self, coords_sequence):
        request = Request("http://localhost:5000/route/v1/car/{0}")
        response = request(self.__to_osrm_literal_coordinates(coords_sequence))

        if response and response['code'] == 'Ok':
            routes = response['routes']
            if len(routes) > 0:
                # Add an overhead for every stop loading/unloading
                stop_service_overhead = len(coords_sequence) * 3
                return routes[0]['duration'] + stop_service_overhead

        return 0

    def __to_osrm_literal_coordinates(self, coords_sequence): 
        formatted_coords = ''
        for i in range(len(coords_sequence)):
            formatted_coords += str(coords_sequence[i][0]) + ',' + str(coords_sequence[i][1])
            if i < len(coords_sequence) - 1:
                formatted_coords += ';'
        
        return formatted_coords

