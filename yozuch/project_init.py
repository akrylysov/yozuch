"""
Project creator.
"""

import os
import shutil
import datetime
from yozuch import config, logger
from yozuch.utils import makedirs


def init(project_dir):
    makedirs(project_dir)

    # Create dirs
    dirs = [
        'assets',
        'documents',
        'posts',
        'templates',
    ]

    for dir_name in dirs:
        makedirs(os.path.join(project_dir, dir_name))

    makedirs(os.path.join(project_dir, 'assets', 'images'))

    # Copy initial post
    post_name = '{0:%Y}-{0:%m}-{0:%d}-demo-post.rst'.format(datetime.datetime.now())
    shutil.copyfile(os.path.join(config.PACKAGE_DIR, 'templates', 'post.rst'),
                    os.path.join(project_dir, 'posts', post_name))

    # Copy sample image
    shutil.copyfile(os.path.join(config.PACKAGE_DIR, 'templates', 'python-powered-w-200x80.png'),
                    os.path.join(project_dir, 'assets', 'images', 'python-powered-w-200x80.png'))

    # Copy about page
    shutil.copyfile(os.path.join(config.PACKAGE_DIR, 'templates', 'about.rst'),
                    os.path.join(project_dir, 'documents', 'about.rst'))

    # Copy initial config
    shutil.copyfile(os.path.join(config.PACKAGE_DIR, 'templates', 'config.py'), os.path.join(project_dir, 'config.py'))

    logger.info('Congratulations! Blog successfully created in {} directory.'.format(project_dir))
