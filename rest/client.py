import typing

import requests

from . import models


class APIV2Client:
    _BASE_ENDPOINT: str = 'https://www.bitstamp.net/api/v2'
    _HTTP_GET: str = 'GET'
    _HTTP_POST: str = 'POST'
    _HTTP_DELETE: str = 'DELETE'
    _HTTP_PATCH: str = 'PATCH'
    _HTTP_PUT: str = 'PUT'

    def __init__(self, client_id: str = None, api_key: str = None, api_secret: str = None):
        pass

    def ticker(self, currency_pair: str) -> str:
        """
        Executes an HTTP request calling latest ticker info.
        :param currency_pair: defines which currency pair to get ticker for.
        """
        return self._make_request(self._HTTP_GET, '/ticker/' + currency_pair)

    def hourly_ticker(self, currency_pair: str) -> str:
        """
        Executes an HTTP request calling hourly ticker info.
        :param currency_pair: defines which currency pair to get hourly ticker for.
        """
        return self._make_request(self._HTTP_GET, '/ticker_hour/' + currency_pair)

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

        params = {'group': group}
        return self._make_request(self._HTTP_GET, '/order_book/' + currency_pair, params)

    def transactions(self, currency_pair: str, period: str = 'hour'):
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
        return self._make_request(self._HTTP_GET, '/transactions/' + currency_pair, params)

    def conversion_rate(self) -> models.ConversionRate:
        """
        Retrieves current BUY/SELL conversion rate for EUR/USD.
        """
        rsp = self._make_request(self._HTTP_GET, '/eur_usd/')
        return models.ConversionRate(rsp)

    @classmethod
    def _make_request(cls, method: str, endpoint: str, params: typing.Dict = None, body: typing.Dict = None,
                      headers: typing.Dict = None):
        """
        Private function for all different HTTP request methods using request library.

        :param method: indicates the HTTP request method (GET, POST,...)
        :param endpoint: specific endpoint for for api endpoints.
        :param params: additional parameters
        :param body: Body of the request
        :param headers: headers of the request.
        :return: json value of response.
        """
        try:
            rsp = {
                cls._HTTP_GET: requests.get(url=cls._BASE_ENDPOINT + endpoint, params=params),
                cls._HTTP_POST: requests.get(url=cls._BASE_ENDPOINT + endpoint, params=params)
            }.get(method)

            if rsp is None:
                raise Exception('Unknown HTTP method')

            return rsp

        except Exception as e:
            raise ValueError('Connection error while making request %s: with endpoint: %s, error: %s', method,
                             endpoint, e)
