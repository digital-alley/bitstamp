import rest
import settings

print('[*] Lets first construct a rest API client.')
client = rest.APIV2Client(
    client_id=settings.CLIENT_ID,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET
)

print('[*] Calling ticker endpoint for BTC/USD currency pair:')
rsp = client.ticker('btcusd')
print(
    'high: {high}, last: {last}, timestamp: {timestamp}, '
    'bid: {bid}, vwap: {vwap}, volume: {volume}, low: {low}, ask: {ask}, open: {open}'.format(high=rsp.high,
                                                                                              last=rsp.last,
                                                                                              timestamp=rsp.timestamp,
                                                                                              bid=rsp.bid,
                                                                                              vwap=rsp.vwap,
                                                                                              volume=rsp.volume,
                                                                                              low=rsp.low,
                                                                                              ask=rsp.ask,
                                                                                              open=rsp.open))

print('[*] Calling hourly ticker endpoint for BTC/USD currency pair:')
rsp = client.hourly_ticker('btceur')
print(
    'high: {high}, last: {last}, timestamp: {timestamp}, '
    'bid: {bid}, vwap: {vwap}, volume: {volume}, low: {low}, ask: {ask}, open: {open}'.format(high=rsp.high,
                                                                                              last=rsp.last,
                                                                                              timestamp=rsp.timestamp,
                                                                                              bid=rsp.bid,
                                                                                              vwap=rsp.vwap,
                                                                                              volume=rsp.volume,
                                                                                              low=rsp.low,
                                                                                              ask=rsp.ask,
                                                                                              open=rsp.open))

print('[*] Calling order_book endpoint for DAI/USD currency pair:')
rsp = client.order_book('daiusd', group=0)
print(
    'timestamp: {timestamp}, microtimestamp: {microtimestamp}'.format(
        timestamp=rsp.timestamp,
        microtimestamp=rsp.microtimestamp))
print('[*] Bids:')
for i in rsp.bids:
    print('price: {price}, amount: {amount}'.format(price=i.price, amount=i.amount))
print('[*] Asks:')
for i in rsp.asks:
    print('price: {price}, amount: {amount}'.format(price=i.price, amount=i.amount))

print('[*] Calling transactions in the last minute endpoint for BTC/USD currency pair:')
rsp = client.transactions('btcusd', period='minute')
for r in rsp:
    print('date: {date}, tid: {tid}, amount: {amount}, type: {type}, price: {price}'.format(date=r.date,
                                                                                            tid=r.tid,
                                                                                            amount=r.amount,
                                                                                            type=r.type,
                                                                                            price=r.price
                                                                                            ))

print('[*] === AUTHORIZED REQUESTS: You need to provide your accout details (api_key, api_secret, client_id) ===')
print('[*] Calling get balances for BTC/EUR')
rsp = client.balances()
print('EUR balance:', rsp.get('eur_balance'), ' BTC balance:', rsp.get('btc_balance'))

print('[*] Calling get order_status')
rsp = client.order_status(123456)
print(rsp)
