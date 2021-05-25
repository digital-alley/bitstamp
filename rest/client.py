import hashlib
import hmac
import time
import typing
import uuid

import requests


class APIV2Client:
    base_endpoint: str = 'https://www.bitstamp.net/api/v2'

    _client_id: str
    _api_key: str
    _api_secret: typing.Union[bytes, bytearray]

    def __init__(self, client_id: str = None, api_key: str = None, api_secret: typing.Union[bytes, bytearray] = None):
        self._client_id = client_id
        self._api_key = api_key
        self._api_secret = api_secret

    def ticker(self, currency_pair: str) -> str:
        """
        Executes an HTTP request calling latest ticker info.
        :param currency_pair: defines which currency pair to get ticker for.
        """
        rsp = requests.get(url=self.base_endpoint + '/ticker/' + currency_pair)
        if rsp.status_code == 404:
            raise ValueError('Ticker for requested currency pair not found.')

        return rsp.json()

    def hourly_ticker(self, currency_pair: str) -> str:
        """
        Executes an HTTP request calling hourly ticker info.
        :param currency_pair: defines which currency pair to get hourly ticker for.
        """

        rsp = requests.get(url=self.base_endpoint + '/ticker_hour/' + currency_pair)
        if rsp.status_code == 404:
            raise ValueError('Ticker for requested currency pair not found.')

        return rsp.json()

    def order_book(self, currency_pair: str, group: int = 1):
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

        rsp = requests.get(url=self.base_endpoint + '/order_book/' + currency_pair, params={'group': group})
        if rsp.status_code == 404:
            raise ValueError('Order book for requested currency pair not found.')

        return rsp.json()

    def _get_auth_headers(self, api_endpoint: str, body: str, method: str, content_type: str = None) -> typing.Dict:
        """
        Creates and returns headers for authorized requests.
        :param api_endpoint: which API endpoint to create headers and signature for
        :param body: string payload of the request
        :param method: http verb for request (GET, POST , ...)
        :param content_type: content type
        :return: Dictionary with AUTH headers.
        """
        if not (self._api_key and self._api_secret and self._client_id):
            raise ValueError('ApiKey, ApiSecret and ClientId all need to be provided in order to authenticate')

        current_milli_timestamp = str(round(time.time() * 1000))
        nonce = str(uuid.uuid4())
        message = 'BITSTAMP {api_key}{method}www.bitstamp.net{api_endpoint}{content_type}{nonce}{timestamp}v2{body}'
        message = message.format(
            api_key=self._api_key, method=method, api_endpoint=api_endpoint, content_type=content_type,
            nonce=nonce, timestamp=current_milli_timestamp, body=body
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
        if content_type is not None:
            headers['Content-Type'] = content_type

        return headers
