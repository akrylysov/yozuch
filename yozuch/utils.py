"""
Helpers.
"""

import os
import shutil
import string
import importlib
from collections import OrderedDict


class ObjectFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        if len(args) < 1 or not isinstance(args[0], object):
            raise TypeError()
        try:
            val = getattr(args[0], key)
        except AttributeError:
            val = args[0][key]
        if val is None:
            raise TypeError("'{}' object attribute '{}' is None".format(args[0], key))
        return val


def format_object(fmt, obj):
    return ObjectFormatter().format(fmt, obj)


def format_url_from_object(fmt, obj):
    url = format_object(fmt, obj)
    if url.endswith('/index/'):
        url = url.replace('/index/', '/')
    return url


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def emptydir(path):
    if not os.path.isdir(path):
        return
    for name in os.listdir(path):
        item_path = os.path.join(path, name)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path, True)


def path_from_url(url):
    path = url.lstrip('/').replace('/', os.path.sep)
    filename = os.path.basename(path)
    return os.path.join(path, 'index.html') if not filename else path


def normalize_slug(s):
    return s.replace(' ', '-').lower()


def unique_list_items(l):
    return list(OrderedDict.fromkeys(l))


def is_external_url(url):
    if url.startswith('//'):
        return True
    schemes = ('http', 'https', 'skype', 'mailto')
    return any([url.startswith(scheme + ':') for scheme in schemes])


def import_module(module_name):
    try:
        return importlib.import_module(module_name)
    except ValueError:
        raise NameError('Unable to import module {}'.format(module_name))


def import_module_member(name):
    parts = name.split('.')
    module_name = '.'.join(parts[:-1])
    member_name = parts[-1]
    return getattr(import_module(module_name), member_name)
