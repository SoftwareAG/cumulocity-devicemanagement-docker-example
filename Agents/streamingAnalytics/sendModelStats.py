import paho.mqtt.client as mqtt
import sys
import os
import subprocess
import jsonify
import logging
import utils.settings
import time
import threading
import json
import API.measurement
import API.authentication as auth
import API.identity
import API.inventory

logger = logging.getLogger('Model Status updater')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for sending Docker Status to Platform')


def main():
        logger.info('Sending new Model stats')
        try:
            time.sleep(int(utils.settings.device()['c8y.model.status.update']))
        except:
            logger.warning('Configurated model update intervall not valid, using 10s instead.')
            time.sleep(10)
        API.inventory.updateManageObject(auth.get().internalID, json.dumps(getStats()))

def start():
    try:
        while True:
            main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        pass

def stop():
    raise Exception

def getStats():
    try:
        rawStats = subprocess.Popen(["docker", "exec", "apama", "ls", "Project_deployed/monitors"],stdout=subprocess.PIPE)
        list = rawStats.stdout.read().decode('utf-8').replace('\n','').split('.mon')
        #list = ['ModelManager', 'MyNewAnalyticsModel', 'ReceiveMQTTRawAndRouteC8YMeasurement', '']
        list = list[:-1]
        a = []
        for i in list:
            dict = {}
            for counter,value in enumerate(i.split(';')):
                if counter == 0:
                    dict["name"] = value
                    dict["status"] = "active"
            a.append(dict)
        payload = {}
        payload['c8y_ThinEdge_Model'] = a
        logger.debug('The following model stats where found: %s'% (str(payload)))
        return payload
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
        raise Exception
