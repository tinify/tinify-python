# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from tinify import ResultMeta

from helper import *

class TinifyResultMetaWithMetaTest(TestHelper):
    def setUp(self):
        self.result = ResultMeta({
            'Image-Width': '100',
            'Image-Height': '60',
            'Content-Length': '20',
            'Content-Type': 'application/json',
            'Location': 'https://bucket.s3-region.amazonaws.com/some/location'
        })

    def test_width_should_return_image_width(self):
        self.assertEqual(100, self.result.width)

    def test_height_should_return_image_height(self):
        self.assertEqual(60, self.result.height)

    def test_location_should_return_stored_location(self):
        self.assertEqual('https://bucket.s3-region.amazonaws.com/some/location', self.result.location)

class TinifyResultMetaWithoutMetaTest(TestHelper):
    def setUp(self):
        self.result = ResultMeta({})

    def test_width_should_return_none(self):
        self.assertEqual(None, self.result.width)

    def test_height_should_return_none(self):
        self.assertEqual(None, self.result.height)

    def test_location_should_return_none(self):
        self.assertEqual(None, self.result.location)
