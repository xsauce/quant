# -*- coding: utf-8 -*-
import logging
from cloghandler import ConcurrentRotatingFileHandler as RFHandler


def create_logger(log_name, log_file=None, log_level='INFO'):
    logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    logger.setLevel(numeric_level)
    if log_file:
        file_hdlr = RFHandler(filename=log_file, maxBytes=100 * 1024 * 1024, backupCount=10)
        file_hdlr.setFormatter(log_formatter)
        logger.addHandler(file_hdlr)
    stream_hdlr = logging.StreamHandler()
    stream_hdlr.setFormatter(log_formatter)
    logger.addHandler(stream_hdlr)
    return logger

if __name__ == '__main__':
    logger = create_logger('example', log_file='/var/log/quant/example.log')
    logger.info('example info')
    logger.warn('1234')