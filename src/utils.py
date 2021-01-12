import logging
from os import environ as env


def get_logger(name=None):
    name = name or __name__
    FORMAT = "%(asctime)s %(name)-4s %(process)d %(levelname)-6s %(funcName)-8s %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger(name)
    if env.get("BE_VERBOSE"):
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logger.setLevel(log_level)
    return logger
