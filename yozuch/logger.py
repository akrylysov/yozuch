"""
Logging helpers.
"""

import logging
import sys


logger = logging.getLogger('yozuch')


class RejectFilter(logging.Filter):

    def __init__(self, reject):
        super().__init__()
        self.reject = reject

    def filter(self, record):
        return not self.reject(record)


def _setup_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)7s] %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.addFilter(RejectFilter(lambda record: record.levelno != logging.INFO))
    logger.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.addFilter(RejectFilter(lambda record: record.levelno == logging.INFO))
    logger.addHandler(stderr_handler)


_setup_logger()
