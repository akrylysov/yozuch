from yozuch.paginator import Paginator
from tests import YozuchTestCase


class PaginatorTest(YozuchTestCase):

    def test_paginator(self):
        paginator = Paginator([1, 2, 3, 4, 5], 2)

        self.assertEqual(paginator.number_of_pages, 3)
        self.assertEqual(len(paginator.pages), 3)

        for i, page in enumerate(paginator.pages, start=1):
            self.assertEqual(page.number, i)

        self.assertEqual(paginator.pages[0].entries, [1, 2])
        self.assertEqual(paginator.pages[1].entries, [3, 4])
        self.assertEqual(paginator.pages[2].entries, [5])