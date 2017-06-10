"""
Site entries.
"""

from yozuch.utils import normalize_slug


def linkitems(objs, reverse=False):
    previtem = None
    if reverse:
        objs = reversed(objs)
    for obj in objs:
        obj.previtem = previtem
        if previtem is not None:
            previtem.nextitem = obj
        previtem = obj
    return objs


class LinkedListItemMixin(object):
    nextitem = None
    previtem = None


class Entry(LinkedListItemMixin):

    _slug = None
    _name = None

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, val):
        self._slug = normalize_slug(val)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.slug = name

    def __init__(self, url):
        self.url = url

    def publish(self, context):
        pass

    def write(self, context, env, output_dir):
        pass


class CollectionItem(Entry):

    def __init__(self, url, name):
        super().__init__(url)
        self.name = name
        self.posts = []

    def __str__(self):
        return self.slug
