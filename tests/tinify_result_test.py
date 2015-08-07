# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from tinify import Result

from . import *

class TinifyResultWithMetaAndDataTest(TestHelper):
  def setUp(self):
    self.result = Result({
        'Image-Width': '100',
        'Image-Height': '60',
        'Content-Length': '450',
        'Content-Type': 'image/png',
      }, b'image data')

  def test_width_should_return_image_width(self):
    self.assertEqual(100, self.result.width)

  def test_height_should_return_image_height(self):
    self.assertEqual(60, self.result.height)

  def test_location_should_return_none(self):
    self.assertEqual(None, self.result.location)

  def test_size_should_return_content_length(self):
    self.assertEqual(450, self.result.size)

  def test_len_builtin_should_return_content_length(self):
    self.assertEqual(450, len(self.result))

  def test_content_type_should_return_mime_type(self):
    self.assertEqual('image/png', self.result.content_type)

  def test_to_buffer_should_return_image_data(self):
    self.assertEqual(b'image data', self.result.to_buffer())
