import logging

def getLogger(func, level=logging.DEBUG):
    logger = logging.getLogger(func)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    return logger
