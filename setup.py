import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tinify'))
from version import __version__

tests_require = ['nose', 'httpretty']
if sys.version_info < (2, 7):
    tests_require.append('unittest2')
if sys.version_info < (3, 3):
    tests_require.append('mock')

setup(
    name='tinify',
    version=__version__,
    description='Tinify API client.',
    author='Jacob Middag',
    author_email='jacobmiddag@voormedia.com',
    license='MIT',
    long_description='Python client for the Tinify API. Tinify compresses your images intelligently. Read more at https://tinify.com.',
    url='https://tinify.com/developers',

    packages=['tinify'],
    package_data={
        '': ['LICENSE', 'README.md'],
        'tinify': ['data/cacert.pem'],
    },

    install_requires=['requests'],
    tests_require=tests_require,
    extras_require={'test': tests_require},

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ),
)
