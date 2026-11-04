# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # type: ignore

if TYPE_CHECKING:
    from typing import Final, Literal


class Format(object):
    """Media types that images can be converted to.

    Use these constants with :meth:`Source.convert`::

        tinify.from_file("input.png") \\
            .convert(type=tinify.Format.JXL) \\
            .to_file("output.jxl")

    Multiple types may be supplied, in which case the API returns the
    smallest result::

        .convert(type=[tinify.Format.JXL, tinify.Format.WEBP])

    Each constant is typed as its own literal, so they satisfy the
    :data:`~tinify._typed.ConvertTypes` hints that :meth:`Source.convert`
    accepts.
    """

    #: WebP.
    WEBP = "image/webp"  # type: Final[Literal["image/webp"]]

    #: PNG.
    PNG = "image/png"  # type: Final[Literal["image/png"]]

    #: JPEG.
    JPEG = "image/jpeg"  # type: Final[Literal["image/jpeg"]]

    #: JPEG, under the alternative ``image/jpg`` media type the API also
    #: accepts. The API normalises this to ``image/jpeg``, so the result is
    #: identical to :attr:`JPEG`. The two constants hold different strings
    #: but select the same format.
    JPG = "image/jpg"  # type: Final[Literal["image/jpg"]]

    #: AVIF.
    AVIF = "image/avif"  # type: Final[Literal["image/avif"]]

    #: JPEG XL.
    JXL = "image/jxl"  # type: Final[Literal["image/jxl"]]

    #: Wildcard, returns the smallest of the supported types.
    ANY = "*/*"  # type: Final[Literal["*/*"]]

    def __init__(self):
        # type: () -> None
        raise TypeError("Format is a namespace of constants and cannot be instantiated")
