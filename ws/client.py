import websocket
import json
import threading
import typing


class WebsocketV2Client(threading.Thread):
    _worker: websocket.WebSocketApp
    _channels: typing.List[str]

    _WS_ENDPOINT = 'wss://ws.bitstamp.net/'

    def __init__(self, channels: typing.List[str], callback=None):
        super().__init__()
        self._channels = channels
        self._worker = websocket.WebSocketApp(self._WS_ENDPOINT,
                                              on_open=self.on_open,
                                              on_message=self.on_message,
                                              on_error=self.on_error,
                                              on_close=self.on_close)

        self._msg_received_callback = callback

    def run(self):
        self._worker.run_forever()

    def subscribe_to_channel(self, channel: str):
        subscribe_msg = {
            'event': 'bts:subscribe',
            'data': {
                'channel': '{0}'.format(channel)
            }
        }
        json_msg = json.dumps(subscribe_msg)
        self._worker.send(json_msg)

    def unsubscribe_from_channel(self, channel: str):
        unsubscribe_msg = {
            'event': 'bts:unsubscribe',
            'data': {
                'channel': '{0}'.format(channel)
            }
        }

        json_msg = json.dumps(unsubscribe_msg)
        self._worker.send(json_msg)

    def on_message(self, ws, message):
        """
        Interface method that determines what happens on recevied message
        """
        if self._msg_received_callback:
            self._msg_received_callback(message)

    def on_error(self, ws, error):
        """
        Interface method that determines what happens on error
        """
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print('Connection closed')

    def on_open(self, ws):
        for channel in self._channels:
            self.subscribe_to_channel(channel)
