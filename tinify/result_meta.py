# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from requests.structures import CaseInsensitiveDict

try:
    from typing import Optional, Dict
except ImportError:
    pass



class ResultMeta(object):
    def __init__(self, meta):  # type: (CaseInsensitiveDict[str]) -> None
        self._meta = meta

    @property
    def width(self):  # type: () -> Optional[int]
        value = self._meta.get('Image-Width')
        return int(value) if value else None

    @property
    def height(self):  # type: () -> Optional[int]
        value = self._meta.get('Image-Height')
        return int(value) if value else None

    @property
    def location(self):  # type: () -> Optional[str]
        return self._meta.get('Location')

    @property
    def size(self):  # type: () -> Optional[int]
        value = self._meta.get('Content-Length')
        return int(value) if value else None

    def __len__(self):  # type: () -> int
        return self.size or 0
