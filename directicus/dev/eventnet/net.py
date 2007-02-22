import struct
import cStringIO
import gherkin as encoder
from twisted.internet import protocol, reactor
import driver

class StringQueue(object):
    def __init__(self):
        self.l_buffer = []
        self.s_buffer = ""

    def write(self, data):
        self.l_buffer.append(data)

    def read(self, count=None):
        if count > len(self.s_buffer) or count==None:
            self.build_s_buffer()
        result = self.s_buffer[:count]
        self.s_buffer = self.s_buffer[count:]
        return result

    def build_s_buffer(self):
        new_string = "".join(self.l_buffer)
        self.s_buffer = "".join((self.s_buffer, new_string))
        self.l_buffer = []

    def __len__(self):
        self.build_s_buffer()
        return len(self.s_buffer)

def message_unpacker(data):
    while True:
        if len(data) >= 4:
            size = struct.unpack("!l", data.read(4))[0]
            while len(data) < size:
                yield None
            message = data.read(size)
            yield message
        else:
            yield None

def pack_message(data):
    size = struct.pack("!l", len(data))
    return "".join((size, data))

class MessageProtocol(protocol.Protocol):
    def __init__(self, *args, **kw):
        self.buffer = StringQueue()
        self.message_unpacker = message_unpacker(self.buffer)
        self.callbacks = {}

    def connectionMade(self):
        if self.factory.handleNewConnection:
            self.factory.handleNewConnection(self)

    def connectionLost(self, reason):
        if self.factory.handleCloseConnection:
            self.factory.handleCloseConnection(self)

    def post(self, name, **kw):
        data = pack_message(encoder.dumps((name, kw)))
        self.transport.write(data)

    def dataReceived(self, data):
        self.buffer.write(data)
        for message in self.message_unpacker:
            if message is not None:
                name, kw = encoder.loads(message)
                kw['_conn'] = self
                kw['reply'] = self.post
                if name == 'NET_RESPONSE':
                    self.callbacks[kw['_uid']](kw)
                else:
                    driver.post(name, **kw)
            else: break

    def request(self, name, **kw):
        if 'callback' not in kw:
            raise ValueError, 'callback keyword not supplied.'
        kw['_request'] = name
        kw['_uid'] = self.factory.uid
        self.callbacks[kw['_uid']] = kw['callback']
        del kw['callback']
        self.post('NET_REQUEST', **kw)




class ClientFactory(protocol.ReconnectingClientFactory):
    def __init__(self, onConnect,onClose):
        self.handleNewConnection = onConnect
        self.handleCloseConnection = onClose
        self._uid = 0
        self.maxDelay = 10





    def get_uid(self):
        self._uid += 1
        return self._uid
    uid = property(get_uid)

    def buildProtocol(self, addr):
        self.resetDelay()
        p = MessageProtocol()
        p.factory = self
        return p


class ServerFactory(protocol.ServerFactory):
    def __init__(self, onConnect,onClose):
        self.handleNewConnection = onConnect
        self.handleCloseConnection = onClose
        self._uid = 0

    def get_uid(self):
        self._uid += 1
        return self._uid
        uid = property(get_uid)

    def buildProtocol(self, addr):
        p = MessageProtocol()
        p.factory = self
        return p


def listen(port, onConnect, onClose):
    reactor.listenTCP(port, ServerFactory(onConnect, onClose))

def connect(address, port,onConnect, onClose):
    reactor.connectTCP(address, port, ClientFactory(onConnect, onClose))

poll = reactor.iterate

if __name__ == "__main__":
    pass
