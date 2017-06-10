import unittest
import logging
import sys
import os
from contextlib import contextmanager
from io import StringIO
from yozuch import logger
from yozuch.config import Config


class MockLoggingHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }


class YozuchTestCase(unittest.TestCase):

    ROOT_DIR = os.path.dirname(__file__)

    def setUp(self):
        self.logger_handler = MockLoggingHandler()
        self._orig_handlers = logger.handlers
        logger.handlers = []
        logger.addHandler(self.logger_handler)
        self.config = Config(os.path.join(self.ROOT_DIR, 'data'))

    def tearDown(self):
        logger.handlers = self._orig_handlers

    def _is_logger_errors(self):
        return len(self.logger_handler.messages['error']) > 0 or len(self.logger_handler.messages['critical']) > 0


@contextmanager
def capture_stdout():
    stdout_orig = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out
        yield out
    finally:
        sys.stdout = stdout_orig
