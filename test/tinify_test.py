# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from base64 import b64encode

import tinify
from helper import *

class TinifyKey(TestHelper):
    def test_should_reset_client_with_new_key(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/')
        tinify.key = 'abcde'
        tinify.get_client()
        tinify.key = 'fghij'
        tinify.get_client().request('GET', '/')
        self.assertEqual(self.request.headers['authorization'], 'Basic {0}'.format(
           b64encode(b'api:fghij').decode('ascii')))

class TinifyAppIdentifier(TestHelper):
    def test_should_reset_client_with_new_app_identifier(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/')
        tinify.key = 'abcde'
        tinify.app_identifier = 'MyApp/1.0'
        tinify.get_client()
        tinify.app_identifier = 'MyApp/2.0'
        tinify.get_client().request('GET', '/')
        self.assertEqual(self.request.headers['user-agent'], tinify.Client.USER_AGENT + " MyApp/2.0")

class TinifyClient(TestHelper):
    def test_with_key_should_return_client(self):
        tinify.key = 'abcde'
        self.assertIsInstance(tinify.get_client(), tinify.Client)

    def test_without_key_should_raise_error(self):
        with self.assertRaises(tinify.AccountError):
            tinify.get_client()

class TinifyValidate(TestHelper):
    def test_with_valid_key_should_return_true(self):
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink', status=400,
            body='{"error":"InputMissing","message":"No input"}')
        tinify.key = 'valid'
        self.assertEqual(True, tinify.validate())

    def test_with_error_should_raise_error(self):
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink', status=401,
            body='{"error":"Unauthorized","message":"Credentials are invalid"}')
        tinify.key = 'valid'
        with self.assertRaises(tinify.AccountError):
            tinify.validate()

class TinifyFromBuffer(TestHelper):
    def test_should_return_source(self):
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink',
            location='https://api.tinify.com/some/location')
        tinify.key = 'valid'
        self.assertIsInstance(tinify.from_buffer('png file'), tinify.Source)

class TinifyFromFile(TestHelper):
    def test_should_return_source(self):
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink',
            location='https://api.tinify.com/some/location')
        tinify.key = 'valid'
        self.assertIsInstance(tinify.from_file(dummy_file), tinify.Source)
