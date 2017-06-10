"""
Paginator.
"""

import math
from yozuch.entries import LinkedListItemMixin, linkitems


class PaginatorPage(LinkedListItemMixin):

    def __init__(self, number, entries):
        self.entries = entries
        self.number = number
        self.url = None


class Paginator(object):

    def __init__(self, entries, entries_per_page):
        self.number_of_pages = int(math.ceil(float(len(entries)) / entries_per_page))
        self.pages = []
        for i in range(self.number_of_pages):
            self.pages.append(PaginatorPage(i+1, entries[i*entries_per_page:(i+1)*entries_per_page]))
        linkitems(self.pages, True)
