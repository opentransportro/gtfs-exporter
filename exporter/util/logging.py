import logging

from exporter.settings import LOG_LEVEL


def init_logging():
    logging.basicConfig()
    logging.getLogger().setLevel(LOG_LEVEL)

    logger = logging.getLogger('gtfsexporter')
    logger.setLevel(LOG_LEVEL)
        
    # sh = logging.StreamHandler(sys.stdout)
    # logger.addHandler(sh)
