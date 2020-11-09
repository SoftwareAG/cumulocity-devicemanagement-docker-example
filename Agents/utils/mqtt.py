import configparser
from os import path
import logging
import os
import paho.mqtt.client as paho

logger = logging.getLogger('MQTT')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for MQTT send module')

configCredentials = configparser.ConfigParser()
configCredentials.read('./config/config.ini')

def mqttSend(topic, payload):
    logger.info('Starting mqtt send')
    client = paho.Client()
    broker = configCredentials['MQTT']['broker']
    logger.info('MQTT Broker is: ' + str(broker))
    port = configCredentials['MQTT']['port']
    logger.info('MQTT Broker port is: ' + str(port))
    client.connect(broker, int(port), 60)
    logger.info('Connecting')
    logger.debug('Sending the following payload: ' + str(payload))
    logger.debug('Sending on the following topic: ' + str(topic))
    client.publish(topic, payload)
    logger.info('Publishing')
    client.disconnect()
