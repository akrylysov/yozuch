"""
Default configuration and configuration related helpers.
"""

import os
import importlib.util
from yozuch.view import view


PACKAGE_DIR = os.path.dirname(__file__)


class DefaultConfig(object):

    DEBUG = False

    TITLE = 'Site title'
    URL = 'http://localhost:8000'
    DESCRIPTION = 'Site description'
    AUTHOR = 'Name Surname'

    THEME_NAME = None
    THEME_CONFIG = {}
    THEME_DEFAULT_TEMPLATES = {
        'blog-index': 'blog_index.html',
        'posts': 'post.html',
        'tags-index': 'tags_index.html',
        'tags': 'tag.html',
        'archive-index': 'archive_index.html',
        'atom-feed': 'atom.xml',
        'documents': 'document.html',
    }

    RST_OPTIONS = {
        'meta_date_format': '%Y-%m-%d',
        'filename_meta_formats': [
            '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)',
            '(?P<slug>.*)'
        ],
        'filename_meta_date_format': '%Y-%m-%d',
        'file_extensions': ['.rst'],
        'add_heading_permalink': False,
        'permalink_text': '&#x00b6;',
    }

    PAGE_FILE_EXTENSIONS = ['.html', '.xml']

    LOADERS = [
        ('yozuch.loaders.post.PostLoader', {}),
        ('yozuch.loaders.document.DocumentLoader', {}),
        ('yozuch.loaders.page.PageLoader', {}),
        ('yozuch.loaders.asset.AssetLoader', {}),
    ]

    PLUGINS = [
        'yozuch.plugins.video',
        'yozuch.plugins.speakerdeck',
    ]

    VIEWS = (
        view('/', 'blog-index'),
        view('/blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/', 'posts'),
        view('/tags/', 'tags-index'),
        view('/tag/{slug}/', 'tags'),
        view('/archive/', 'archive-index'),
        view('/{slug}/', 'documents'),
        view('/atom.xml', 'atom-feed'),
        view('/{filename}', 'assets'),
    )


class Config(dict):

    KEYS_TO_MERGE = ['RST_OPTIONS', 'THEME_CONFIG', 'THEME_DEFAULT_TEMPLATES']

    def __init__(self, directory, config_overrides=None):
        super().__init__()
        self.update_from_object(DefaultConfig)
        self.update_from_directory(directory)
        if config_overrides is not None:
            self.update_from_dict(config_overrides)

    def update_from_object(self, other, **kwargs):
        self.update_from_dict({key: getattr(other, key) for key in dir(other) if key.isupper()}, **kwargs)

    def update_from_dict(self, other, replace_duplicates=True):
        for key, value in other.items():
            if key.isupper():
                if key in self.KEYS_TO_MERGE and self.get(key):
                    if not replace_duplicates:
                        other[key].update(self[key])
                    self[key].update(other[key])
                else:
                    self[key] = other[key]

    def update_from_directory(self, source_dir, **kwargs):
        spec = importlib.util.spec_from_file_location('user_config', os.path.join(source_dir, 'config.py'))
        if spec is None:
            return
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.update_from_object(mod, **kwargs)
