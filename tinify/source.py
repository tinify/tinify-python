# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import tinify
import sys
from tinify.result import Result
from tinify.result_meta import ResultMeta

try:
    from typing import Union, Dict, IO, Any, Unpack, TYPE_CHECKING, overload
    if sys.version_info.major > 3 and sys.version_info.minor > 8:
        from  tinify._typed import *
except ImportError:
    TYPE_CHECKING = False # type: ignore

class Source(object):
    @classmethod
    def from_file(cls, path):  # type: (Union[str, IO]) -> Source
        if hasattr(path, 'read'):
            return cls._shrink(path)
        else:
            with open(path, 'rb') as f:
                return cls._shrink(f.read())

    @classmethod
    def from_buffer(cls, string):  # type: (bytes) -> Source
        return cls._shrink(string)

    @classmethod
    def from_url(cls, url):  # type: (str) -> Source
        return cls._shrink({"source": {"url": url}})

    @classmethod
    def _shrink(cls, obj):  # type: (Any) -> Source
        response = tinify.get_client().request('POST', '/shrink', obj)
        return cls(response.headers['location'])

    def __init__(self, url, **commands):  # type: (str, **Any) -> None
        self.url = url
        self.commands = commands

    def preserve(self, *options):  # type: (*PreserveOption) -> "Source"
        return type(self)(self.url, **self._merge_commands(preserve=self._flatten(options)))

    def resize(self, **options):  # type: (Unpack[ResizeOptions]) -> "Source"
        return type(self)(self.url, **self._merge_commands(resize=options))

    def convert(self, **options):  # type: (Unpack[ConvertOptions]) -> "Source"
        return type(self)(self.url, **self._merge_commands(convert=options))

    def transform(self, **options):  # type: (Unpack[TransformOptions]) -> "Source"
        return type(self)(self.url, **self._merge_commands(transform=options))

    if TYPE_CHECKING:
        @overload
        def store(self, **options): # type: (Unpack[S3StoreOptions]) -> ResultMeta
            pass

        @overload
        def store(self, **options): # type: (Unpack[GCSStoreOptions]) -> ResultMeta
            pass

    def store(self, **options):  # type: (Any) -> ResultMeta
        response = tinify.get_client().request('POST', self.url, self._merge_commands(store=options))
        return ResultMeta(response.headers)

    def result(self):  # type: () -> Result
        response = tinify.get_client().request('GET', self.url, self.commands)
        return Result(response.headers, response.content)

    def to_file(self, path):  # type: (Union[str, IO]) -> None
        return self.result().to_file(path)

    def to_buffer(self):  # type: () -> bytes
        return self.result().to_buffer()

    def _merge_commands(self, **options):  # type: (**Any) -> Dict[str, Any]
        commands = self.commands.copy()
        commands.update(options)
        return commands

    def _flatten(self, items, seqtypes=(list, tuple)):
        items = list(items)
        for i, x in enumerate(items):
            while isinstance(items[i], seqtypes):
                items[i:i+1] = items[i]
        return items
