# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import sys
try:
    from typing import Optional, Any, TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False # type: ignore

class tinify(object):

    _client = None  # type: Optional[Client]
    _key = None  # type: Optional[str]
    _app_identifier = None  # type: Optional[str]
    _proxy = None  # type: Optional[str]
    _compression_count = None  # type: Optional[int]

    def __init__(self, module):
        # type: (Any) -> None
        self._module = module
        self._lock = threading.RLock()

        self._client = None
        self._key = None
        self._app_identifier = None
        self._proxy = None
        self._compression_count = None

    @property
    def key(self):
        # type: () -> Optional[str]
        return self._key

    @key.setter
    def key(self, value):
        # type: (str) -> None
        self._key = value
        self._client = None

    @property
    def app_identifier(self):
        # type: () -> Optional[str]
        return self._app_identifier

    @app_identifier.setter
    def app_identifier(self, value):
        # type: (str) -> None
        self._app_identifier = value
        self._client = None

    @property
    def proxy(self):
        # type: () -> Optional[str]
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        # type: (str) -> None
        self._proxy = value
        self._client = None

    @property
    def compression_count(self):
        # type: () -> Optional[int]
        return self._compression_count

    @compression_count.setter
    def compression_count(self, value):
        # type: (int) -> None
        self._compression_count = value

    def get_client(self):
        # type: () -> Client
        if not self._key:
            raise AccountError('Provide an API key with tinify.key = ...')

        if not self._client:
            with self._lock:
                if not self._client:
                    self._client = Client(self._key, self._app_identifier, self._proxy)

        return self._client

    # Delegate to underlying base module.
    def __getattr__(self, attr):
        # type: (str) -> Any
        return getattr(self._module, attr)

    def validate(self):
        # type: () -> bool
        try:
            self.get_client().request('post', '/shrink')
        except AccountError as err:
            if err.status == 429:
                return True
            raise err
        except ClientError:
            return True
        return False

    def from_file(self, path):
        # type: (str) -> Source
        return Source.from_file(path)

    def from_buffer(self, string):
        # type: (bytes) -> Source
        return Source.from_buffer(string)

    def from_url(self, url):
        # type: (str) -> Source
        return Source.from_url(url)

if TYPE_CHECKING:
    # Help the type checker here, as we overrride the module with a singleton object.
    def get_client(): # type: () -> Client
        pass
    key = None  # type: Optional[str]
    app_identifier = None  # type: Optional[str]
    proxy = None  # type: Optional[str]
    compression_count = None  # type: Optional[int]

    def validate():  # type: () -> bool
        pass

    def from_file(path):  # type: (str) -> Source
        pass

    def from_buffer(string):  # type: (bytes) -> Source
        pass

    def from_url(url):  # type: (str) -> Source
        pass


# Overwrite current module with singleton object.
tinify = sys.modules[__name__] = tinify(sys.modules[__name__])  # type: ignore

from .version import __version__

from .client import Client
from .result_meta import ResultMeta
from .result import Result
from .source import Source
from .errors import *

__all__ = [
    'Client',
    'Result',
    'ResultMeta',
    'Source',
    'Error',
    'AccountError',
    'ClientError',
    'ServerError',
    'ConnectionError'
]
