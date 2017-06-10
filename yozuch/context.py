import datetime
import os
from yozuch.config import Config, PACKAGE_DIR


class Context(object):

    def __init__(self, config_overrides, project_path, output_dir=None):
        self.config = config = Config(project_path, config_overrides)
        self.project_path = project_path
        self.theme = config['THEME_CONFIG']
        self.site = {
            # config aliases
            'url': config['URL'],
            'title': config['TITLE'],
            'author': config['AUTHOR'],
            'description': config['DESCRIPTION'],

            # current time
            'time': datetime.datetime.now(),
        }
        self.entries = {}
        self.references = {}

        self.theme_path = os.path.join(project_path, 'themes', config['THEME_NAME'])
        if not os.path.isdir(self.theme_path):
            self.theme_path = os.path.join(PACKAGE_DIR, 'themes', config['THEME_NAME'])

        self.templates_path = os.path.join(project_path, 'templates')
        self.pages_dir = os.path.join(project_path, 'pages')
        self.output_path = os.path.join(project_path, output_dir or 'output')
