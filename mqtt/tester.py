import click
import json
from client import MQTTClient
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.task import LoopingCall
import time

class Listener(ReconnectingClientFactory):

    def __init__(self, service=None, packets=None):
        self.service = service
        self.protocol = MQTTClient
        self.packets = packets
        

    def buildProtocol(self, addr):
<<<<<<< HEAD
        proto = self.protocol(packets=self.packets)
=======
        proto = self.protocol(packets=self.packets, clientId="������")
>>>>>>> fix
        proto.factory = self
        self.protocol = proto
        return proto

    def clientConnectionLost(self, connector, reason):
        print("CONNESSIONE PERSA: {}".format(reason))
        self.protocol = MQTTClient
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("CONNESSIONE FALLITA: {}".format(reason))
        self.protocol = MQTTClient

        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    """def publish(self, topic, message):
        if self.protocol != MQTTClient:
            self.protocol.publish(topic, message)"""

    


@click.command()
@click.option('--host', default="localhost", help='L\'host del broker MQTT', show_default=True)
@click.option('--port', default=1883, help="La porta del broker MQTT", show_default=True)
@click.option('--packets', default="", help="Lista dei pacchetti da inviare", show_default=True)

def hello(host, port, packets):
    with open(packets, mode='r') as f:
        loadedPackets = json.load(f)
    mqttListener = Listener(packets=loadedPackets)
    reactor.connectTCP(host, port, mqttListener)
    reactor.run()
    

if __name__ == '__main__':
    hello()