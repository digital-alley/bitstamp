import hashlib
import hmac
import time
import uuid
from urllib.parse import urlencode
import typing
import json
import requests

from . import models


class APIV2Client:
    _DOMAIN: str = 'www.bitstamp.net'
    _BASE_URL: str = 'https://www.bitstamp.net'

    _HTTP_GET: str = 'GET'
    _HTTP_POST: str = 'POST'
    _HTTP_DELETE: str = 'DELETE'
    _HTTP_PATCH: str = 'PATCH'
    _HTTP_PUT: str = 'PUT'

    _client_id: str
    _api_key: str
    _api_secret: typing.Union[bytes, bytearray]

    def __init__(self, client_id: str = None, api_key: str = None, api_secret: str = None):
        self._client_id = client_id
        self._api_key = api_key
        self._api_secret = bytes(api_secret.encode('utf-8'))

    def ticker(self, currency_pair: str) -> models.Ticker:
        """
        Executes an HTTP request calling latest ticker info.
        :param currency_pair: defines which currency pair to get ticker for.
        """
        rsp = self._make_request(self._HTTP_GET, '/api/v2/ticker/' + currency_pair)
        serialized = models.rsp_to_dict(rsp)

        return models.Ticker(serialized)

    def hourly_ticker(self, currency_pair: str) -> models.Ticker:
        """
        Executes an HTTP request calling hourly ticker info.
        :param currency_pair: defines which currency pair to get hourly ticker for.
        """
        rsp = self._make_request(self._HTTP_GET, '/api/v2/ticker_hour/' + currency_pair)
        serialized = models.rsp_to_dict(rsp)

        return models.Ticker(serialized)

    def order_book(self, currency_pair: str, group: int = 1) -> models.OrderBook:
        """
        Retrieves current order book snapshot for specified currency pair. It also supports 3 states of
        order grouping.

        :param currency_pair: defines which order book to get order_book for.
        :param group: defines how order book is grouped.
        0 - orders are not grouped at the same price.
        1 - orders are grouped at the same price (default)
        2 - order with their order ids are not grouped at the same price
        """
        if group not in [0, 1, 2]:
            raise ValueError('Group parameter should be 0, 1 or 2.')

        params = {'group': group}
        rsp = self._make_request(self._HTTP_GET, '/api/v2/order_book/' + currency_pair, params)
        serialized = models.rsp_to_dict(rsp)

        return models.OrderBook(serialized)

    def transactions(self, currency_pair: str, period: str = 'hour') -> typing.List[models.Transaction]:
        """
        Returns descending list of transactions for specified currency pair. Supports time interval from which we want the transactions
        to be returned.

        :param currency_pair:  defines which currency pair to get transactions for.
        :param period: defines the time interval.
        minute - returns transactions for last minute.
        hour - returns transactions for the hour.
        day - returns transactions for the day.
        """
        params = {'time': period}
        rsp = self._make_request(self._HTTP_GET, '/api/v2/transactions/' + currency_pair, params)
        serialized = models.rsp_to_dict(rsp)
        transactions = []
        for s in serialized:
            transactions.append(models.Transaction(s))

        return transactions

    def conversion_rate(self) -> models.ConversionRate:
        """
        Retrieves current BUY/SELL conversion rate for EUR/USD.
        """
        rsp = self._make_request(self._HTTP_GET, '/api/v2/eur_usd/')
        return models.ConversionRate(rsp)

    def balances(self, currency_pair: str = None) -> typing.Dict:
        """
        Returns balance for specified currency pair. If currency pair is not specified, it returns
        balance data for all available currency pairs.

        :param currency_pair:  defines which currency pair to get balance for.
        :return: dict with balance data
        """
        endpoint = '/api/v2/balance/'
        if currency_pair is not None:
            endpoint += currency_pair + '/'

        rsp = self._make_request(self._HTTP_POST, endpoint, is_authorized=True)

        return json.loads(rsp.text)

    def order_status(self, order_id: int):
        """
        Returns status for the specified order id.

        :param order_id:  an id for requested order status.
        :return: dict with balance data
        """
        rsp = self._make_request(self._HTTP_POST, '/api/v2/order_status/', payload={'id': order_id},
                                 content_type='application/x-www-form-urlencoded', is_authorized=True)

        return json.loads(rsp.text)

    def _make_request(self, method: str, endpoint: str, params: typing.Dict = None, payload: typing.Dict = None,
                      headers: typing.Dict = None, is_authorized=False, content_type: str = ''):
        """
        Private function for all different HTTP request methods using request library.

        :param method: indicates the HTTP request method (GET, POST,...)
        :param endpoint: specific endpoint for for api endpoints.
        :param params: additional parameters
        :param body: Body of the request
        :param headers: headers of the request.
        :return: json value of response.
        """
        req_headers = {}
        if is_authorized:
            req_headers = self._get_auth_headers(endpoint, method, params, payload, content_type)
        if headers:
            req_headers.update(headers)
        try:
            rsp = {
                self._HTTP_GET: requests.get(url=self._BASE_URL + endpoint, params=params, headers=req_headers),
                self._HTTP_POST: requests.post(url=self._BASE_URL + endpoint, params=params, data=payload,
                                               headers=req_headers)
            }.get(method)

            if rsp is None:
                raise Exception('Unknown HTTP method')

            return rsp

        except Exception as e:
            raise ValueError('Connection error while making request %s: with endpoint: %s, error: %s', method,
                             endpoint, e)

    def _get_auth_headers(
            self, endpoint: str, method: str, params: typing.Dict = None,
            payload: typing.Dict = None, content_type: str = '') -> typing.Dict:
        """
        Creates and returns headers for authorized requests.
        :param api_endpoint: which API endpoint to create headers and signature for
        :param body: string payload of the request
        :param method: http verb for request (GET, POST , ...)
        :param content_type: content type
        :return: Dictionary with AUTH headers.
        """
        if not (self._api_key and self._api_secret and self._client_id):
            raise ValueError('api_key, api_secret and client_id all need to be provided in order to authenticate')

        current_milli_timestamp = str(round(time.time() * 1000))
        nonce = str(uuid.uuid4())
        raw_message = 'BITSTAMP {api_key}{method}{base_url}{api_endpoint}{params}{content_type}{nonce}{date}v2{payload}'
        payload_string = urlencode(payload) if payload is not None else ''
        query = ''
        if params is not None:
            query = '?'
            for key, value in params.items():
                query += str(key) + '=' + str('value') + '&'
            query = query[:-1]
        message = raw_message.format(
            api_key=self._api_key, method=method, base_url=self._DOMAIN, api_endpoint=endpoint, params=query,
            content_type=content_type,
            nonce=nonce, date=current_milli_timestamp, payload=payload_string
        )
        message = message.encode('utf-8')
        signature = hmac.new(self._api_secret, msg=message, digestmod=hashlib.sha256).hexdigest()
        headers = {
            'X-Auth': 'BITSTAMP {0}'.format(self._api_key),
            'X-Auth-Signature': signature,
            'X-Auth-Nonce': nonce,
            'X-Auth-Timestamp': str(current_milli_timestamp),
            'X-Auth-Version': 'v2'
        }
        if content_type:
            headers['Content-Type'] = content_type

        return headers
