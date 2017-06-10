import os
from tests import YozuchTestCase
from yozuch.config import Config


class ConfigTest(YozuchTestCase):

    def test_merge(self):
        config = Config(os.path.join(self.ROOT_DIR, 'data'))
        self.assertEqual(config['THEME_CONFIG']['foo'], 'bar')

        config.update_from_dict({'FOO': 'baz'})
        self.assertEqual(config['FOO'], 'baz')
        config.update_from_directory(os.path.join(self.ROOT_DIR, 'data', 'themes', 'test'), replace_duplicates=False)
        self.assertEqual(config['FOO'], 'baz')
        self.assertEqual(config['THEME_CONFIG']['foo'], 'bar')
        self.assertEqual(config['THEME_CONFIG']['baz'], 'qux')
        self.assertTrue(config['DEBUG'])
        self.assertEqual(config['THEME_NAME'], 'test')

        self.assertRaises(NameError, lambda: config.update_from_directory(os.path.join(self.ROOT_DIR, 'data-invalid')))
