import sys
import logging
from os import path
from os import remove
import requests
import streamingAnalytics.listener
import deviceRegistration.registrationProcess
import API.authentication as auth
import API.identity
import time
import threading
import utils.settings
import dockerWatcher.sendDockerStats
import streamingAnalytics.sendModelStats
import utils.threadCommunication as communication
import deviceStatus.sendDeviceStats
import streamingAnalytics.modelSync
import paho.mqtt.publish as publish
import deviceControl.operationsListener
import deviceControl.smartRest



logger = logging.getLogger('deviceAgent')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for deviceAgent was initialised')

def checkUsabilityCredentials():
    logger.info('Cecking if available credentials work')
    url = "https://%s/user/currentUser"%(auth.get().tenant)
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers)
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Credentials valid')
        return True
    else:
        logger.info('Deleting Credential File')
        remove("./config/credentials.key")
        return False

def start():
    logger.info('Checking for credentials')
    if not path.exists('./config/credentials.key'):
        logger.info('No credentials found, starting registration')
        deviceRegistration.registrationProcess.start()
    logger.info('Credentials available')
    logger.info('Starting checking of existing device')
    if API.identity.getInternalID(utils.settings.basics()['deviceID']) is False:
        logger.info('No device found in c8y, starting edge device creation.')
        deviceRegistration.newDeviceRegistration.createEdgeDevice(utils.settings.basics()['deviceID'])
    auth.get().internalID = API.identity.getInternalID(utils.settings.basics()['deviceID'])
    utils.settings.device()
    deviceControl.smartRest.checkSmartRestTemplateExists()
    streamingAnalytics.modelSync.models()
    logger.info('Sending internalID on MQTT for APAMA standalone')
    try:
        publish.single("settings/internalID", str(auth.get().internalID), hostname=utils.settings.mqtt()['broker'], port=int(utils.settings.mqtt()['port']))
    except:
        logger.warning('No MQTT Broker yet available')
    logger.info('Finishing start sequency')


def operation():
    logger.info('Starting operationsWatcher')
    threadOperatiosnWatcher = threading.Thread(target=deviceControl.operationsListener.start, daemon=True)
    threadOperatiosnWatcher.start()
    return threadOperatiosnWatcher

def listener():
    logger.info('Starting listener')
    threadMQTTListener = threading.Thread(target=streamingAnalytics.listener.start, daemon=True)
    threadMQTTListener.start()
    return threadMQTTListener

def dockerStatus():
    logger.info('Starting Docker Status')
    threadDockerStatus = threading.Thread(target=dockerWatcher.sendDockerStats.start, daemon=True)
    threadDockerStatus.start()
    return threadDockerStatus

def modelStatus():
    logger.info('Starting Model Status')
    threadModelStatus = threading.Thread(target=streamingAnalytics.sendModelStats.start, daemon=True)
    threadModelStatus.start()
    return threadModelStatus

def deviceStatsStatus():
    logger.info('Starting Device Status')
    threadDeviceStatus = threading.Thread(target=deviceStatus.sendDeviceStats.start, daemon=True)
    threadDeviceStatus.start()
    return threadDeviceStatus


if __name__== "__main__":
    try:
        start()
        statusDevice = deviceStatsStatus()
        statusOperation = operation()
        #statusListener = listener()
        #statusDocker = dockerStatus()
        #statusModel = modelStatus()
        while True:
            time.sleep(1)
            print("Heartbeat")
            """"if statusListener.is_alive() is False:
                logger.error('Listener on Measurements not alive, restarting')
                time.sleep(5)
                statusListerner = listener()"""
            if statusOperation.is_alive() is False:
                logger.error('Listener on operations not alive, restarting')
                time.sleep(5)
                statusOperation = operation()
            """elif statusDocker.is_alive() is False:
                logger.error('Status on Docker not alive, restarting')
                time.sleep(5)
                statusDocker = dockerStatus()
            elif statusModel.is_alive() is False:
                logger.error('Status on Model not alive, restarting')
                time.sleep(5)
                statusModel = modelStatus()
            elif statusDevice.is_alive() is False:
                logger.error('Status on device update not alive, restarting')
                time.sleep(5)
                statusDevice = deviceStatsStatus()"""
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        pass
