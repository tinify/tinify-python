# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import sys
import os
import httpretty
from nose.exc import SkipTest

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

for code in (584, 543, 492, 401):
    httpretty.http.STATUSES.setdefault(code)

dummy_file = os.path.join(os.path.dirname(__file__), 'examples', 'dummy.png')

import tinify

class RaiseException(object):
    def __init__(self, exception):
        self.exception = exception

    def __call__(self, *args, **kwargs):
        raise self.exception

class TestHelper(unittest.TestCase):
    def setUp(self):
        httpretty.enable()
        httpretty.HTTPretty.allow_net_connect = False

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

        tinify.key = None
        tinify.app_identifier = None
        tinify.proxy = None
        tinify.compression_count

    def assertJsonEqual(self, expected, actual):
        self.assertEqual(json.loads(expected), json.loads(actual))

    @property
    def request(self):
        return httpretty.last_request()
