import os
from yozuch.loaders.rstloader import RstLoader
from tests import YozuchTestCase


class LoaderTest(YozuchTestCase):

    def setUp(self):
        super(LoaderTest, self).setUp()
        self.loader = RstLoader(self.config['RST_OPTIONS'])

    def test_posts(self):
        posts = list(self.loader.load_documents(os.path.join(self.ROOT_DIR, 'data', 'posts')))
        self.assertEqual(len(posts), 3)
        self.assertEqual(len(self.logger_handler.messages['error']), 1)

    def test_posts_empty(self):
        posts = list(self.loader.load_documents(os.path.join(self.ROOT_DIR, 'data')))
        self.assertEqual(len(posts), 0)
        self.assertFalse(self._is_logger_errors())
