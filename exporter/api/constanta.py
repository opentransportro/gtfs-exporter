import logging

from gtfslib.model import Agency

from exporter.api.radcom import RadcomApiDataProvider

logger = logging.getLogger("gtfsexporter")


class ConstantaApiDataProvider(RadcomApiDataProvider):
    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__("https://info.ctbus.ro/rp/api", feed_id, lenient, disable_normalization, **kwargs)

    def _load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        stb = Agency(self.feed_id, 1, "Regia AAutonomă de Transport în Comun Constanța", "https://ctbus.ro",
                     "Europe/Bucharest", **{
                "agency_lang": "ro",
                "agency_email": "contact@ctbus.ro",
                "agency_fare_url": "https://www.ctbus.ro/#Tarife",
                "agency_phone": "0241694960"
            })

        # add here safe insert
        self.dao.session().merge(stb)
        self.agency_ids.add(stb.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 1)
        pass
