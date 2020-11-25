import paho.mqtt.client as mqtt
import sys
import os
import jsonify
import logging
import utils.settings
import time
import threading
import json
import API.measurement
import API.authentication as auth
import API.identity

logger = logging.getLogger('Listener')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for MQTT listenerwas initialised')

def event(topic, payload):
    try:
        message = json.loads(payload)
        if 'source' in str(message):
            message['source']['id'] = str(auth.get().internalID)
            logger.info('The following topic arrived %s', payload)
            API.measurement.createMeasurement(json.dumps(message))
        else:
            raise ValueError
    except ValueError as e:
        return logger.error('Not valid json or valid structure')
    except Exception as e:
        logger.error('The following error occured: ' + str(e))


def on_message_msgs(mosq, obj, msg):
    #print("Withing Callback")
    # This callback will only be called for messages with topics that matchs the assigned topics
    try:
        logger.debug('Callback function was initiated')
        logger.info('The following topic triggered a callback function: %s', msg.topic)
        logger.info('The following payload arrived: %s', msg.payload)
        logger.debug('Object with Event-Class will be created')
        threadEvent = threading.Thread(target=event, kwargs=dict(topic=msg.topic,payload=msg.payload), daemon=True)
        threadEvent.start()
    except Exception as e:
        logger.error('The following error occured: ' + str(e))


def main():
    try:
        logger.debug('Setting prefix within MQTT broker for machine from config file')
        mqttSettings = utils.settings.mqtt()
        logger.debug('Initialising MQTT client with loaded credentials for listener')
        client = mqtt.Client()
        logger.info('MQTT client with loaded credentials was initialised')
        topicAggregated = str(utils.settings.device()['c8y.aggregated.apama.topic'])
        topicSignalType = str(utils.settings.device()['c8y.signaltype.apama.topic'])
        logger.info('Listening for callback on all messsages on topic %s: ', topicAggregated)
        logger.info('Listening for callback on all messsages on topic %s: ', topicSignalType)
        client.message_callback_add(topicAggregated, on_message_msgs)
        client.message_callback_add(topicSignalType, on_message_msgs)
        logger.info('Connecting to MQTT Broker')
        client.connect(mqttSettings['broker'], int(mqttSettings['port']), 60)
        client.subscribe("#", 0)
        logger.info('Start Loop forever and listening')
        client.loop_forever()
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        client.stop_loop()
        logger.warning('Loop forever stopped, disconnecting')
        client.disconnect()
        logger.debug('disconnected')

def start():
    try:
        while True:
            main()
            logger.error('Main loop left')
            time.sleep(10)
        logger.error('Main loop left')
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        pass

def stop():
    print("Stopping")
