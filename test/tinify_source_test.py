# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import json
import tempfile

import tinify
from tinify import Source, Result, ResultMeta, AccountError, ClientError

from helper import *

class TinifySourceWithInvalidApiKey(TestHelper):
    def setUp(self):
        super(type(self), self).setUp()
        tinify.key = 'invalid'
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink', **{
          'status': 401
        })

    def test_from_file_should_raise_account_error(self):
        with self.assertRaises(AccountError):
            Source.from_file(dummy_file)

    def test_from_buffer_should_raise_account_error(self):
        with self.assertRaises(AccountError):
            Source.from_buffer('png file')

    def test_from_url_should_raise_account_error(self):
        with self.assertRaises(AccountError):
            Source.from_url('http://example.com/test.jpg')

class TinifySourceWithValidApiKey(TestHelper):
    def setUp(self):
        super(type(self), self).setUp()
        tinify.key = 'valid'
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink', **{
          'status': 201,
          'location': 'https://api.tinify.com/some/location'
        })
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/some/location', body=self.return_file)
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/some/location', body=self.return_file)

    @staticmethod
    def return_file(request, uri, headers):
        if request.body:
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = {}
        response = None
        if 'store' in data:
            headers['location'] = 'https://bucket.s3-region.amazonaws.com/some/location'
            response = json.dumps({'status': 'success'}).encode('utf-8')
        elif 'preserve' in data:
            response = b'copyrighted file'
        elif 'resize' in data:
            response = b'small file'
        else:
            response = b'compressed file'
        return (200, headers, response)

    def test_from_file_with_path_should_return_source(self):
        self.assertIsInstance(Source.from_file(dummy_file), Source)

    def test_from_file_with_path_should_return_source_with_data(self):
        self.assertEqual(b'compressed file', Source.from_file(dummy_file).to_buffer())

    def test_from_file_with_file_object_should_return_source(self):
        with open(dummy_file, 'rb') as f:
            self.assertIsInstance(Source.from_file(f), Source)

    def test_from_file_with_file_object_should_return_source_with_data(self):
        with open(dummy_file, 'rb') as f:
            self.assertEqual(b'compressed file', Source.from_file(f).to_buffer())

    def test_from_buffer_should_return_source(self):
        self.assertIsInstance(Source.from_buffer('png file'), Source)

    def test_from_buffer_should_return_source_with_data(self):
        self.assertEqual(b'compressed file', Source.from_buffer('png file').to_buffer())

    def test_from_url_should_return_source(self):
        self.assertIsInstance(Source.from_url('http://example.com/test.jpg'), Source)

    def test_from_url_should_return_source_with_data(self):
        self.assertEqual(b'compressed file', Source.from_url('http://example.com/test.jpg').to_buffer())

    def test_from_url_should_raise_error_when_server_doesnt_return_a_success(self):
        httpretty.register_uri(httpretty.POST, 'https://api.tinify.com/shrink',
            body='{"error":"Source not found","message":"Cannot parse URL"}',
            status=400,
        )
        with self.assertRaises(ClientError):
            Source.from_url('file://wrong')

    def test_result_should_return_result(self):
        self.assertIsInstance(Source.from_buffer('png file').result(), Result)

    def test_preserve_should_return_source(self):
        self.assertIsInstance(Source.from_buffer('png file').preserve("copyright", "location"), Source)
        self.assertEqual(b'png file', httpretty.last_request().body)

    def test_preserve_should_return_source_with_data(self):
        self.assertEqual(b'copyrighted file', Source.from_buffer('png file').preserve("copyright", "location").to_buffer())
        self.assertJsonEqual('{"preserve":["copyright","location"]}', httpretty.last_request().body.decode('utf-8'))

    def test_preserve_should_return_source_with_data_for_array(self):
        self.assertEqual(b'copyrighted file', Source.from_buffer('png file').preserve(["copyright", "location"]).to_buffer())
        self.assertJsonEqual('{"preserve":["copyright","location"]}', httpretty.last_request().body.decode('utf-8'))

    def test_preserve_should_return_source_with_data_for_tuple(self):
        self.assertEqual(b'copyrighted file', Source.from_buffer('png file').preserve(("copyright", "location")).to_buffer())
        self.assertJsonEqual('{"preserve":["copyright","location"]}', httpretty.last_request().body.decode('utf-8'))

    def test_preserve_should_include_other_options_if_set(self):
        self.assertEqual(b'copyrighted file', Source.from_buffer('png file').resize(width=400).preserve("copyright", "location").to_buffer())
        self.assertJsonEqual('{"preserve":["copyright","location"],"resize":{"width":400}}', httpretty.last_request().body.decode('utf-8'))

    def test_resize_should_return_source(self):
        self.assertIsInstance(Source.from_buffer('png file').resize(width=400), Source)
        self.assertEqual(b'png file', httpretty.last_request().body)

    def test_resize_should_return_source_with_data(self):
        self.assertEqual(b'small file', Source.from_buffer('png file').resize(width=400).to_buffer())
        self.assertJsonEqual('{"resize":{"width":400}}', httpretty.last_request().body.decode('utf-8'))

    def test_store_should_return_result_meta(self):
        self.assertIsInstance(Source.from_buffer('png file').store(service='s3'), ResultMeta)
        self.assertJsonEqual('{"store":{"service":"s3"}}', httpretty.last_request().body.decode('utf-8'))

    def test_store_should_return_result_meta_with_location(self):
        self.assertEqual('https://bucket.s3-region.amazonaws.com/some/location',
            Source.from_buffer('png file').store(service='s3').location)
        self.assertJsonEqual('{"store":{"service":"s3"}}', httpretty.last_request().body.decode('utf-8'))

    def test_store_should_include_other_options_if_set(self):
        self.assertEqual('https://bucket.s3-region.amazonaws.com/some/location', Source.from_buffer('png file').resize(width=400).store(service='s3').location)
        self.assertJsonEqual('{"store":{"service":"s3"},"resize":{"width":400}}', httpretty.last_request().body.decode('utf-8'))

    def test_to_buffer_should_return_image_data(self):
        self.assertEqual(b'compressed file', Source.from_buffer('png file').to_buffer())

    def test_to_file_with_path_should_store_image_data(self):
        with tempfile.TemporaryFile() as tmp:
            Source.from_buffer('png file').to_file(tmp)
            tmp.seek(0)
            self.assertEqual(b'compressed file', tmp.read())

    def test_to_file_with_file_object_should_store_image_data(self):
        with create_named_tmpfile() as name:
            Source.from_buffer('png file').to_file(name)
            with open(name, 'rb') as f:
                self.assertEqual(b'compressed file', f.read())