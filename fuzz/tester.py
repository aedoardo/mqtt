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
        proto = self.protocol(packets=self.packets, clientId="������")
        proto.factory = self
        self.protocol = proto
        return proto

    def clientConnectionLost(self, connector, reason):
        print("CONNECTION LOST: {}".format(reason))
        self.protocol = MQTTClient
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("CONNECTION FAILED: {}".format(reason))
        self.protocol = MQTTClient

        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    """def publish(self, topic, message):
        if self.protocol != MQTTClient:
            self.protocol.publish(topic, message)"""

    


@click.command()
@click.option('--host', default="localhost", help='MQTT Broker address', show_default=True)
@click.option('--port', default=1883, help="MQTT Broker port", show_default=True)
@click.option('--packets', default="", help="List of packets to send", show_default=True)

def hello(host, port, packets):
    with open(packets, mode='r') as f:
        loadedPackets = json.load(f)
    mqttListener = Listener(packets=loadedPackets)
    reactor.connectTCP(host, port, mqttListener)
    reactor.run()
    

if __name__ == '__main__':
    hello()