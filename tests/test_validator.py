import os
from tests import YozuchTestCase
from yozuch.validator import validate


class ValidatorTest(YozuchTestCase):

    def test_validate(self):
        validate(self.config, os.path.join(self.ROOT_DIR, 'compiled-data-validator'))
        expected_warnings = [
            'Unable to find reference test.HTML in test.html',
            'Unable to find reference unknown_proto:test in test.html',
            'Unable to find reference test.jpg in test.html',
        ]
        warnings = self.logger_handler.messages['warning']
        self.assertEqual(set(expected_warnings), set(warnings))
