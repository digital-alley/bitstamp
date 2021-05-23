import requests


class APIV2Client:
    base_endpoint: str = 'https://www.bitstamp.net/api/v2'

    def __init__(self, client_id: str = None, api_key: str = None, api_secret: str = None):
        pass

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
