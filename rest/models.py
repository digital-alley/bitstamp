import decimal
import json
import typing
from collections import namedtuple

OrderBookEntry = namedtuple('OrderBookEntry', 'price amount')

import requests


def rsp_to_dict(response: requests.Response):
    return json.loads(response.content)


class ConversionRate:
    buy: decimal.Decimal
    sell: decimal.Decimal

    def __init__(self, response: requests.Response):
        dict_rsp = json.loads(response.content)
        self.buy = dict_rsp.get('buy')
        self.sell = dict_rsp.get('sell')


class Ticker:
    high: decimal.Decimal
    last: decimal.Decimal
    timestamp: str
    bid: decimal.Decimal
    vwap: decimal.Decimal
    volume: decimal.Decimal
    low: decimal.Decimal
    ask: decimal.Decimal
    open: decimal.Decimal

    def __init__(self, response: typing.Dict):
        self.high = response.get('high')
        self.last = response.get('last')
        self.timestamp = response.get('timestamp')
        self.bid = response.get('bid')
        self.vwap = response.get('vwap')
        self.volume = response.get('volume')
        self.low = response.get('low')
        self.ask = response.get('ask')
        self.open = response.get('open')


class OrderBook:
    timestamp: str
    microtimestamp: str
    bids: typing.List[OrderBookEntry]
    asks: typing.List[OrderBookEntry]

    def __init__(self, response: typing.Dict):
        self.timestamp = response.get('timestamp')
        self.microtimestamp = response.get('microtimestamp')
        self.bids = self._serialize_order_book_entries(response.get('bids'))
        self.asks = self._serialize_order_book_entries(response.get('asks'))

    @staticmethod
    def _serialize_order_book_entries(entries: typing.List[typing.List[str]]) -> typing.List[OrderBookEntry]:
        serialized = []
        for entry in entries:
            serialized.append(OrderBookEntry(entry[0], entry[1]))
        return serialized


class Transaction:
    date: str
    tid: str
    amount: str
    type: str
    price: str

    def __init__(self, response: typing.Dict):
        self.date = response.get('date')
        self.tid = response.get('tid')
        self.amount = response.get('amount')
        self.type = response.get('type')
        self.price = response.get('price')
