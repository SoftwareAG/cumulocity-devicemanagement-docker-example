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
import API.operations

logger = logging.getLogger('Operation Listener')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger on MQTT for DeviceControl was initialised')

def on_message_msgs(mosq, obj, msg):
    # This callback will only be called for messages with topics that matchs the assigned topics
    logger.debug('Callback function was initiated')
    logger.info('The following payload arrived: %s', msg.payload)
    logger.debug('Object with Event-Class will be created')
    triggerPendingOPerations()

def triggerPendingOPerations():
    try:
        threadEvent = threading.Thread(target=API.operations.getPendingOperations, kwargs=dict(
            internalID=str(auth.get().internalID)), daemon=True)
        threadEvent.start()
    except Exception as e:
        logger.error('The following error occured: ' + str(e))

def main():
    try:
        logger.debug('Setting prefix within MQTT broker for machine from config file')
        logger.debug('Initialising MQTT client with loaded credentials for listener')
        logger.info(utils.settings.basics()['deviceID'])
        client = mqtt.Client(client_id=utils.settings.basics()['deviceID'])
        logger.info('MQTT client with loaded credentials was initialised')
        client.username_pw_set(
            username=auth.get().MqttUser, password=auth.get().MqttPwd)
        logger.info('Listening for callback on s/ds')
        client.message_callback_add('s/ds', on_message_msgs)
        client.message_callback_add('s/dc/c8y_ThinEdge', on_message_msgs)
        logger.info('Connecting to MQTT Broker')
        client.connect(auth.get().tenant, 1883, 60)
        topics = [("s/ds", 0), ("s/dc/c8y_ThinEdge", 0)]
        client.subscribe(topics)
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
        logger.info('Initially starting triggering of getting all pending operations')
        triggerPendingOPerations()
        while True:
            logger.debug(
                'Starting main loop')
            main()
            logger.error('Main loop left')
            time.sleep(10)
        logger.error('Main loop left')
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        pass
