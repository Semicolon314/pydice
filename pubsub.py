from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
import random

def makeId():
  return "%016x" % random.randrange(16**16)

class PubProtocol(basic.LineReceiver):
  def __init__(self, factory):
    self.factory = factory
    self.id = makeId()

  def connectionMade(self):
    self.factory.clients.add(self)
    if self.factory.host == None:
      self.factory.host = self.id
      
    self.sendLine("ID=%s" % self.id)
    self.sendLine("HOST=%s" % self.factory.host)

  def connectionLost(self, reason):
    self.factory.clients.remove(self)

  def lineReceived(self, line):
    for c in self.factory.clients:
      c.sendLine("<{}> {}".format(self.id, line))

class PubFactory(protocol.Factory):
  def __init__(self):
    self.clients = set()
    self.host = None

  def buildProtocol(self, addr):
    return PubProtocol(self)

def startServer(port):
  endpoints.serverFromString(reactor, "tcp:%d" % port).listen(PubFactory())
  reactor.run()

if __name__ == "__main__":
  startServer(31234)