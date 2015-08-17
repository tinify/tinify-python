# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import json
import tempfile

import tinify
from tinify import Source, Result, ResultMeta, AccountError

from . import *

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
        if 'resize' in data:
            response = b'small file'
        elif 'store' in data:
            headers['location'] = 'https://bucket.s3-region.amazonaws.com/some/location'
            response = json.dumps({'status': 'success'}).encode('utf-8')
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

    def test_result_should_return_result(self):
        self.assertIsInstance(Source.from_buffer('png file').result(), Result)

    def test_resize_should_return_source(self):
        self.assertIsInstance(Source.from_buffer('png file').resize(width=400), Source)

    def test_resize_should_return_source_with_data(self):
        self.assertEqual(b'small file', Source.from_buffer('png file').resize(width=400).to_buffer())

    def test_store_should_return_result_meta(self):
        self.assertIsInstance(Source.from_buffer('png file').store(), ResultMeta)

    def test_store_should_return_result_meta_with_location(self):
        self.assertEqual('https://bucket.s3-region.amazonaws.com/some/location',
            Source.from_buffer('png file').store(service='s3').location)

    def test_to_buffer_should_return_image_data(self):
        self.assertEqual(b'compressed file', Source.from_buffer('png file').to_buffer())

    def test_to_file_with_path_should_store_image_data(self):
        (handle, tmp) = tempfile.mkstemp()
        os.close(handle)
        try:
            Source.from_buffer('png file').to_file(tmp)
            with open(tmp, 'rb') as f:
                self.assertEqual(b'compressed file', f.read())
        finally:
            os.unlink(tmp)

    def test_to_file_with_file_object_should_store_image_data(self):
        (handle, tmp) = tempfile.mkstemp()
        os.close(handle)
        try:
            with open(tmp, 'wb') as f:
                Source.from_buffer('png file').to_file(f)
            with open(tmp, 'rb') as f:
                self.assertEqual(b'compressed file', f.read())
        finally:
            os.unlink(tmp)
