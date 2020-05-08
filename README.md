# GTFS EXPORTER/PROCESSOR
**GTFS processing and validator tool based on ```gtfslib-python```**

**Dependencies**:
 - gtfslib - root library that this tool is based on, 
 - clint - use for interacting with cli, 
 - pandas - for advanced csv processing, 
 - pygithub - used to deploy data to github, 
 - environs - use to read environment variables
 
---

### Generating shapes
- for shape generation ```pfaedle``` is required to be installed on the host machine
- to download and build pfaedle proceed to [opentransportro/pfaedle](https://github.com/opentransportro/pfaedle)

### Required environment variables
- ```GH_TOKEN``` - github token for pushing data to git after finishing build
- ```GH_REPO``` - github repo specifing where to push data to. Should be ```user/repo```


### Required call parameters:
```shell script
gtfs-exporter - GTFS to GTFS' conversion tool and database loader
Usage:
  gtfs-process (--provider=<provider> | --delete | --list ) [--url=<url>] [--file=<file>] [--id=<id>]
                        [--logsql] [--lenient] [--schema=<schema>]
                        [--disablenormalize]
  gtfs-process (-h | --help)
  gtfs-process --version
Options:
  --provider=<provider> The provider type. Can be file, url or api.
  --url=<url>
  --file=<file>
  --delete             Delete feed.
  --list               List all feeds.
  --id=<id>            Set the feed ID in case multiple GTFS are to be loaded.
  -h --help            Show help on options.
  --version            Show lib / program version.
  --logsql             Enable SQL logging (very verbose)
  --lenient            Allow some level of brokenness in GTFS input.
  --schema=<schema>    Set the schema to use (for PostgreSQL).
  --disablenormalize   Disable shape and stop times normalization. Be careful
                       if you use this option, as missing stop times will not
                       be interpolated, and shape_dist_traveled will not be
                       computed or converted to meters.
Examples:
  gtfs-process --provider=url --url=https://xxxx --id=feedname
        Load GTFS from url using id "sncf", deleting previous data.
  gtfs-process --delete --id=moontransit
        Delete the "moontransit" feed from the database.
  gtfs-process --list
        List all feed IDs from database
```