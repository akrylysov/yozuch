import os
import shutil
import datetime
from tests import YozuchTestCase, capture_stdout
from yozuch.__main__ import run
from yozuch import __version__ as yozuch_version
from yozuch.project_init import init
from yozuch.loaders.rstloader import RstLoader


class CmdArguments(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CmdTest(YozuchTestCase):

    def test_version(self):
        with capture_stdout() as out:
            run(CmdArguments(command='version'))
        self.assertEqual(out.getvalue(), yozuch_version + '\n')

    def test_init(self):
        loader = RstLoader(self.config['RST_OPTIONS'])
        project_dir = os.path.join(self.ROOT_DIR, 'temp')

        init(project_dir)

        expected_dirs = [
            'assets',
            'documents',
            'posts',
            'templates',
        ]

        for dir_name in expected_dirs:
            self.assertTrue(os.path.isdir(os.path.join(project_dir, dir_name)))

        post_name = '{0:%Y}-{0:%m}-{0:%d}-demo-post.rst'.format(datetime.datetime.now())
        about_page_name = 'about.rst'
        expected_files = [
            os.path.join(project_dir, 'posts', post_name),
            os.path.join(project_dir, 'documents', about_page_name),
            os.path.join(project_dir, 'config.py')
        ]

        for path in expected_files:
            self.assertTrue(os.path.isfile(path))

        post = next(loader.load_documents(os.path.join(project_dir, 'posts')))
        self.assertEqual(post.slug, 'demo-post')
        self.assertFalse(self._is_logger_errors())

        page = next(loader.load_documents(os.path.join(project_dir, 'documents')))
        self.assertEqual(page.slug, 'about')
        self.assertFalse(self._is_logger_errors())

        shutil.rmtree(project_dir, True)
