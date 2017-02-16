# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from base64 import b64encode

import tinify
from tinify import Client, AccountError, ClientError, ConnectionError, ServerError
import requests

from helper import *

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

Client.RETRY_DELAY = 10

class TinifyClientRequestWhenValid(TestHelper):
    def setUp(self):
        super(type(self), self).setUp()
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', **{
          'compression-count': 12
        })

    def test_should_issue_request(self):
        Client('key').request('GET', '/')

        self.assertEqual(self.request.headers['authorization'], 'Basic {0}'.format(
           b64encode(b'api:key').decode('ascii')))

    def test_should_issue_request_without_body_when_options_are_empty(self):
        Client('key').request('GET', '/', {})

        self.assertEqual(self.request.body, b'')

    def test_should_issue_request_without_content_type_when_options_are_empty(self):
        Client('key').request('GET', '/', {})

        self.assertIsNone(self.request.headers.get('content-type'))

    def test_should_issue_request_with_json_body(self):
        Client('key').request('GET', '/', {'hello': 'world'})

        self.assertEqual(self.request.headers['content-type'], 'application/json')
        self.assertEqual(self.request.body, b'{"hello":"world"}')

    def test_should_issue_request_with_user_agent(self):
        Client('key').request('GET', '/')

        self.assertEqual(self.request.headers['user-agent'], Client.USER_AGENT)

    def test_should_update_compression_count(self):
        Client('key').request('GET', '/')

        self.assertEqual(tinify.compression_count, 12)

class TinifyClientRequestWhenValidWithAppId(TestHelper):
    def setUp(self):
        super(type(self), self).setUp()
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', **{
          'compression-count': 12
        })

    def test_should_issue_request_with_user_agent(self):
        Client('key', 'TestApp/0.2').request('GET', '/')

        self.assertEqual(self.request.headers['user-agent'], Client.USER_AGENT + ' TestApp/0.2')

class TinifyClientRequestWhenValidWithProxy(TestHelper):
    def setUp(self):
        super(type(self), self).setUp()
        httpretty.register_uri(httpretty.CONNECT, 'http://localhost:8080', **{
          'compression-count': 12
        })

    def test_should_issue_request_with_proxy_authorization(self):
        raise SkipTest('https://github.com/gabrielfalcao/HTTPretty/issues/122')
        Client('key', None, 'http://user:pass@localhost:8080').request('GET', '/')

        self.assertEqual(self.request.headers['proxy-authorization'], 'Basic dXNlcjpwYXNz')

class TinifyClientRequestWithTimeoutRepeatedly(TestHelper):
    @patch('requests.sessions.Session.request', RaiseException(requests.exceptions.Timeout))
    def test_should_raise_connection_error(self):
        with self.assertRaises(ConnectionError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Timeout while connecting', str(context.exception))

    @patch('requests.sessions.Session.request', RaiseException(requests.exceptions.Timeout))
    def test_should_raise_connection_error_with_cause(self):
        with self.assertRaises(ConnectionError) as context:
            Client('key').request('GET', '/')
        self.assertIsInstance(context.exception.__cause__, requests.exceptions.Timeout)

class TinifyClientRequestWithTimeoutOnce(TestHelper):
    @patch('requests.sessions.Session.request')
    def test_should_issue_request(self, mock):
        mock.side_effect = RaiseException(requests.exceptions.Timeout, num=1)
        mock.return_value.status_code = 201
        mock.return_value = requests.Response()
        self.assertIsInstance(Client('key').request('GET', '/', {}), requests.Response)

class TinifyClientRequestWithConnectionErrorRepeatedly(TestHelper):
    @patch('requests.sessions.Session.request', RaiseException(requests.exceptions.ConnectionError('connection error')))
    def test_should_raise_connection_error(self):
        with self.assertRaises(ConnectionError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Error while connecting: connection error', str(context.exception))

    @patch('requests.sessions.Session.request', RaiseException(requests.exceptions.ConnectionError('connection error')))
    def test_should_raise_connection_error_with_cause(self):
        with self.assertRaises(ConnectionError) as context:
            Client('key').request('GET', '/')
        self.assertIsInstance(context.exception.__cause__, requests.exceptions.ConnectionError)

class TinifyClientRequestWithConnectionErrorOnce(TestHelper):
    @patch('requests.sessions.Session.request')
    def test_should_issue_request(self, mock):
        mock.side_effect = RaiseException(requests.exceptions.ConnectionError, num=1)
        mock.return_value.status_code = 201
        mock.return_value = requests.Response()
        self.assertIsInstance(Client('key').request('GET', '/', {}), requests.Response)

class TinifyClientRequestWithSomeErrorRepeatedly(TestHelper):
    @patch('requests.sessions.Session.request', RaiseException(RuntimeError('some error')))
    def test_should_raise_connection_error(self):
        with self.assertRaises(ConnectionError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Error while connecting: some error', str(context.exception))

class TinifyClientRequestWithSomeErrorOnce(TestHelper):
    @patch('requests.sessions.Session.request')
    def test_should_issue_request(self, mock):
        mock.side_effect = RaiseException(RuntimeError('some error'), num=1)
        mock.return_value.status_code = 201
        mock.return_value = requests.Response()
        self.assertIsInstance(Client('key').request('GET', '/', {}), requests.Response)

class TinifyClientRequestWithServerErrorRepeatedly(TestHelper):
    def test_should_raise_server_error(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', status=584,
            body='{"error":"InternalServerError","message":"Oops!"}')

        with self.assertRaises(ServerError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Oops! (HTTP 584/InternalServerError)', str(context.exception))

class TinifyClientRequestWithServerErrorOnce(TestHelper):
    def test_should_issue_request(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/',
            responses=[
                httpretty.Response(body='{"error":"InternalServerError","message":"Oops!"}', status=584),
                httpretty.Response(body='all good', status=201),
            ])

        response = Client('key').request('GET', '/')
        self.assertEqual('201', str(response.status_code))

class TinifyClientRequestWithBadServerResponseRepeatedly(TestHelper):
    def test_should_raise_server_error(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', status=543,
            body='<!-- this is not json -->')

        with self.assertRaises(ServerError) as context:
            Client('key').request('GET', '/')

        msg = r'Error while parsing response: .* \(HTTP 543/ParseError\)'
        self.assertRegexpMatches(str(context.exception), msg)

class TinifyClientRequestWithBadServerResponseOnce(TestHelper):
    def test_should_issue_request(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/',
            responses=[
                httpretty.Response(body='<!-- this is not json -->', status=543),
                httpretty.Response(body='all good', status=201),
            ])

        response = Client('key').request('GET', '/')
        self.assertEqual('201', str(response.status_code))

class TinifyClientRequestWithClientError(TestHelper):
    def test_should_raise_client_error(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', status=492,
            body='{"error":"BadRequest","message":"Oops!"}')

        with self.assertRaises(ClientError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Oops! (HTTP 492/BadRequest)', str(context.exception))

class TinifyClientRequestWithBadCredentialsResponse(TestHelper):
    def test_should_raise_account_error(self):
        httpretty.register_uri(httpretty.GET, 'https://api.tinify.com/', status=401,
            body='{"error":"Unauthorized","message":"Oops!"}')

        with self.assertRaises(AccountError) as context:
            Client('key').request('GET', '/')
        self.assertEqual('Oops! (HTTP 401/Unauthorized)', str(context.exception))
