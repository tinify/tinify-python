# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from . import Tinify

class Result(object):
    def __init__(self, meta, data):
        self.meta = meta
        self.data = data

    def to_file(self, path):
        if hasattr(path, 'write'):
            path.write(self.data)
        else:
            with open(path, 'wb') as f:
                f.write(self.data)

    def to_buffer(self):
        return self.data

    @property
    def width(self):
        return int(self.meta['Image-Width'])

    @property
    def height(self):
        return int(self.meta['Image-Height'])

    @property
    def size(self):
        return int(self.meta['Content-Length'])

    def __len__(self):
        return self.size

    @property
    def media_type(self):
        return self.meta['Content-Type']

    @property
    def content_type(self):
        return self.media_type
