"""
Validates URLs in generated content.
"""

import os
import codecs
import re
from yozuch import logger
from yozuch.utils import path_from_url, is_external_url

_ALLOWED_EXTENSIONS = ('.html', '.xml')
_URL_FORMAT = '(?:href|src)=["\'](?P<url>[^"\']+?)["\']'


def validate(config, directory):
    logger.info('Validating {}...'.format(directory))
    regex = re.compile(_URL_FORMAT)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext not in _ALLOWED_EXTENSIONS:
                continue
            path = os.path.join(root, filename)
            relpath = os.path.relpath(path, directory)
            with codecs.open(path, 'r', 'utf-8') as f:
                for url in regex.findall(f.read()):
                    url = url.replace(config['URL'], '')
                    url = url.split('#')[0]  # remove hash
                    if not is_external_url(url):
                        resource_path = os.path.join(directory, path_from_url(url))
                        if not os.path.isfile(resource_path) \
                                or os.path.basename(resource_path) not in os.listdir(os.path.dirname(resource_path)):
                            logger.warning('Unable to find reference {} in {}'.format(url, relpath))
