import decimal
import json

import requests


class ConversionRate:
    buy: decimal.Decimal
    sell: decimal.Decimal

    def __init__(self, response: requests.Response):
        dict_rsp = json.loads(response.content)
        self.buy = dict_rsp.get('buy')
        self.sell = dict_rsp.get('sell')
