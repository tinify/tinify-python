# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from typing import Optional
except ImportError:
    pass

class Error(Exception):
    @staticmethod
    def create(message, kind, status):  # type: (Optional[str], Optional[str], int) -> Error
        klass = Error  # type: type[Error]
        if status == 401 or status == 429:
            klass = AccountError
        elif status >= 400 and status <= 499:
            klass = ClientError
        elif status >= 400 and status < 599:
            klass = ServerError

        if not message: message = 'No message was provided'
        return klass(message, kind, status)

    def __init__(self, message, kind=None, status=None, cause=None):  # type: (str, Optional[str], Optional[int], Optional[Exception]) -> None
        self.message = message
        self.kind = kind
        self.status = status
        if cause:
            # Equivalent to 'raise err from cause', also supported by Python 2.
            self.__cause__ = cause

    def __str__(self):  # type: () -> str
        if self.status:
            return '{0} (HTTP {1:d}/{2})'.format(self.message, self.status, self.kind)
        else:
            return self.message

class AccountError(Error): pass
class ClientError(Error): pass
class ServerError(Error): pass
class ConnectionError(Error): pass
