# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = '0.9.0'

import threading
import six

class TinifyMeta(type):
  def __init__(cls, name, bases, dct):
    cls._client = None
    cls._lock = threading.RLock()

    cls.app_identifier = None
    cls.compression_count = None
    cls._key = None
    cls.VERSION = __version__

  @property
  def key(cls):
      return cls._key

  @key.setter
  def key(cls, key):
    cls._client = None
    cls._key = key

  @property
  def client(cls):
    if not cls._key:
      raise AccountError('Provide an API key with Tinify.key = ...')

    if not cls._client:
      with cls._lock:
        cls._client = Client(cls._key, cls.app_identifier)

    return cls._client

@six.add_metaclass(TinifyMeta)
class Tinify(object):
  pass

from .client import Client
from .result_meta import ResultMeta
from .result import Result
from .source import Source
from .errors import *

def set_key(key):
  Tinify.key = key

def set_app_identifier(app_identifier):
  Tinify.app_identifier = app_identifier

def from_file(path):
  return Source.from_file(path)

def from_buffer(string):
  return Source.from_buffer(string)

def validate():
    try:
        Tinify.client.request('post', '/shrink')
    except ClientError:
        return True

def compression_count():
    return Tinify.compression_count
