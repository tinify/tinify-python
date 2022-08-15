# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
import json
import sys
import os
import httpretty

if sys.version_info < (3, 3):
    from mock import DEFAULT
else:
    from unittest.mock import DEFAULT

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

for code in (584, 543, 492, 401):
    httpretty.http.STATUSES.setdefault(code)

dummy_file = os.path.join(os.path.dirname(__file__), 'examples', 'dummy.png')

import tinify

class RaiseException(object):
    def __init__(self, exception, num=None):
        self.exception = exception
        self.num = num

    def __call__(self, *args, **kwargs):
        if self.num == 0:
            return DEFAULT
        else:
            if self.num: self.num -= 1
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



@contextmanager
def create_named_tmpfile():
    #  Due to NamedTemporaryFile requiring to be closed when used on Windows
    #   we create our own NamedTemporaryFile contextmanager
    # See note: https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile

    tmp = NamedTemporaryFile(delete=False)
    try:
        tmp.close()
        yield tmp.name
    finally:
        os.unlink(tmp.name)