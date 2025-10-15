import logging

logging.basicConfig(level=logging.INFO)

def log(msg):
    logging.info(msg)

def warn(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)
