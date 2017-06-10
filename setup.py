import os
import re
from setuptools import setup, find_packages


def read_file(path):
    with open(path) as f:
        return f.read()


def get_version():
    with open(os.path.join('yozuch', '__init__.py')) as f:
        matches = re.search("__version__ = '(.+)'", f.read())
        if matches:
            return matches.group(1)
    raise Exception('Unable to find module version')


setup(
    name='Yozuch',
    version=get_version(),
    description='reStructuredText based static blog generator',
    long_description=read_file('README.rst'),
    author='Artem Krylysov',
    author_email='artem@krylysov.com',
    url='https://github.com/akrylysov/yozuch',
    license='BSD',
    keywords='static blog generator reStructuredText',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'docutils>=0.13.1',
        'pygments>=2.2.0',
        'jinja2>=2.9.6',
        'watchdog>=0.8.3',
    ],
    entry_points={
        'console_scripts': [
            'yozuch = yozuch.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Text Processing',
        'Topic :: Communications',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
