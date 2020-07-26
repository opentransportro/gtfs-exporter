import logging

from exporter.gtfs.model import Agency

from exporter.api.radcom import RadcomApiDataProvider

logger = logging.getLogger("gtfsexporter")

SLEEP_TIME = 0

BASE_URL = "https://info.stbsa.ro/rp/api"


class BucharestApiDataProvider(RadcomApiDataProvider):
    # base api url

    def __init__(self, feed_id="", lenient=False, disable_normalization=False, **kwargs):
        super().__init__("https://info.stbsa.ro/rp/api", feed_id, lenient, disable_normalization)
        # Optional, generate empty feed info

    def _load_agencies(self):
        self.agency_ids = set()
        logger.info("Importing agencies...")

        stb = Agency(self.feed_id, 1, "STB SA", "https://stbsa.ro", "Europe/Bucharest", **{
            "agency_lang": "ro",
            "agency_email": "contact@stbsa.ro",
            "agency_fare_url": "http://stbsa.ro/portofel_electronic.php",
            "agency_phone": "0213110595"
        })

        metrorex = Agency(self.feed_id, 2, "METROREX SA", "https://metrorex.ro", "Europe/Bucharest",
                          **{
                              "agency_lang": "ro",
                              "agency_email": "contact@metrorex.ro",
                              "agency_fare_url": "http://metrorex.ro/titluri_de_calatorie_p1381-1",
                              "agency_phone": "0213193601"
                          })
        self._safe_insert(stb)
        self.agency_ids.add(stb.agency_id)

        self._safe_insert(metrorex)
        self.agency_ids.add(metrorex.agency_id)

        self.dao.flush()
        self.dao.commit()
        logger.info("Imported %d agencies" % 2)
