import ws

def msg_received_callback(message):
    """
    Example callback that is passed to WS client for receiving messages.
    """
    print(message)

print('[*] Running example WS Client')
c = ws.WebsocketV2Client(channels=['live_trades_xrpusd', 'live_trades_xrpeur'], callback=msg_received_callback)
c.run()
