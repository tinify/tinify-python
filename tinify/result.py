# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from requests.structures import CaseInsensitiveDict

from . import ResultMeta

try:
    from typing import Union, Optional, IO
except ImportError:
    pass


class Result(ResultMeta):
    def __init__(self, meta, data):  # type: (CaseInsensitiveDict[str], bytes) -> None
        ResultMeta.__init__(self, meta)
        self.data = data

    def to_file(self, path):  # type: (Union[str, IO]) -> None
        if hasattr(path, 'write'):
            path.write(self.data)
        else:
            with open(path, 'wb') as f:
                f.write(self.data)

    def to_buffer(self):  # type: () -> bytes
        return self.data

    @property
    def size(self):  # type: () -> Optional[int]
        value = self._meta.get('Content-Length')
        return int(value) if value is not None else None

    @property
    def media_type(self):  # type: () -> Optional[str]
        return self._meta.get('Content-Type')

    @property
    def extension(self):  # type: () -> Optional[str]
        media_type = self._meta.get('Content-Type')
        if media_type:
            return media_type.split('/')[-1]
        return None

    @property
    def content_type(self):  # type: () -> Optional[str]
        return self.media_type

    @property
    def location(self):  # type: () -> Optional[str]
        return None
