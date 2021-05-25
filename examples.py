import rest

print('[*] Lets first construct a rest API client.')
client = rest.APIV2Client()

print('[*] Calling order_book endpoint for DAI/USD currency pair:')
rsp = client.order_book('daiusd', group=0)
print(rsp)

print('[*] Calling ticker endpoint for BTC/USD currency pair:')
rsp = client.ticker('btcusd')
print(rsp)

print('[*] Calling hourli ticker endpoint for BTC/USD currency pair:')
rsp = client.ticker('btcusd')
print(rsp)

print('[*] Calling EUR/USD conversion rate endpoint:')
rsp = client.conversion_rate()
print(rsp)