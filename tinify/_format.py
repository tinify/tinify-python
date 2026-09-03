# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


class Format(object):
    """Media types that images can be converted to.

    Use these constants with :meth:`Source.convert`::

        tinify.from_file("input.png") \\
            .convert(type=tinify.Format.JXL) \\
            .to_file("output.jxl")

    Multiple types may be supplied, in which case the API returns the
    smallest result::

        .convert(type=[tinify.Format.JXL, tinify.Format.WEBP])
    """

    #: WebP.
    WEBP = "image/webp"

    #: PNG.
    PNG = "image/png"

    #: JPEG.
    JPEG = "image/jpeg"

    #: JPEG, an alias of :attr:`JPEG`.
    JPG = "image/jpg"

    #: AVIF.
    AVIF = "image/avif"

    #: JPEG XL.
    JXL = "image/jxl"

    #: Wildcard, returns the smallest of the supported types.
    ANY = "*/*"

    def __init__(self):
        raise TypeError("Format is a namespace of constants and cannot be instantiated")
