from exporter.gtfs.dao import Dao
from exporter.util.perf import run_command

class Processor:
    def __init__(self):
        pass

class OSRMTimeProcessor(Processor):
    def __init__(self):
        #start docker
        run_command(["docker", "run", "-t",
                     "-v", f"{app_path}:/data",
                     "osrm/osrm-backend",
                     "osrm-routed", "-p", "/opt/car.lua", "/data/map.pbf"
                     ])
    def __del__(self):
        # stop docker
        run_command([])
    def process(self, dao: Dao):
        pass


