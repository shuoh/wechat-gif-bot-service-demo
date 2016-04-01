# -*- coding: utf-8 -*-

import unittest
from gifbot.gif_search.search_services import GifNotFoundException, GoogleGifSearchService


class TestGifSearchService(unittest.TestCase):

    def setUp(self):
        self.service = GoogleGifSearchService()

    def test_search_succeed(self):
        results = self.service.search(u'金馆长')

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        for url in results:
            self.assertIsInstance(url, unicode)

    def test_search_fail(self):
        with self.assertRaises(GifNotFoundException):
            self.service.search(u'asdlfkja;lsdkfja;lskdfja;lsdkjf;alskdjfa;lskdfja;lskdfj;alskdfja;lskdfja;dfj,w')
