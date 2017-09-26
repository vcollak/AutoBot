
from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class CommandsReceiveProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("Connection open...")

    def onMessage(self, payload, isBinary):
        print("Command message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("Connection closed: {0}".format(reason))


if __name__ == '__main__':

    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    factory.protocol = CommandsReceiveProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
