# -*- coding: utf-8 -*-


class Error(Exception):
    @staticmethod
    def create(message, kind, status):
        if status == 401 or status == 429:
            klass = AccountError
        elif 400 <= status <= 499:
            klass = ClientError
        elif 400 <= status < 599:
            klass = ServerError
        else:
            klass = Error

        if not message:
            message = 'No message was provided'
        return klass(message, kind, status)

    def __init__(self, message, kind=None, status=None, cause=None):
        self.message = message
        self.kind = kind
        self.status = status
        if cause:
            # Equivalent to 'raise err from cause', also supported by Python 2.
            self.__cause__ = cause

    def __str__(self):
        if self.status:
            return '{0} (HTTP {1:d}/{2})'.format(self.message, self.status, self.kind)
        else:
            return self.message


class AccountError(Error):
    pass


class ClientError(Error):
    pass


class ServerError(Error):
    pass


class ConnectionError(Error):
    pass
