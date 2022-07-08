import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tinify'))
from version import __version__

install_require = ['requests >= 2.7.0, < 3.0.0']
tests_require = ['pytest', 'httpretty < 1.1.5']

if sys.version_info < (2, 7):
    tests_require.append('unittest2')
if sys.version_info < (3, 3):
    tests_require.append('mock >= 1.3, < 2.0')

setup(
    name='tinify',
    version=__version__,
    description='Tinify API client.',
    author='Jacob Middag',
    author_email='info@tinify.com',
    license='MIT',
    long_description='Python client for the Tinify API. Tinify compresses your images intelligently. Read more at https://tinify.com.',
    long_description_content_type='text/markdown',
    url='https://tinify.com/developers',

    packages=['tinify'],
    package_data={
        '': ['LICENSE', 'README.md'],
        'tinify': ['data/cacert.pem'],
    },

    install_requires=install_require,
    tests_require=tests_require,
    extras_require={'test': tests_require},

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ),
)
