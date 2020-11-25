# coding=utf-8
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

logger = logging.getLogger('Docker Status updater')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for sending Docker Status to Platform')


def main():
    try:
        logger.info('Sending new Docker stats')
        try:
            time.sleep(int(utils.settings.device()['c8y.docker.status.update']))
        except:
            logger.warning('Configurated docker update intervall not valid, using 10s instead.')
            time.sleep(10)
        API.inventory.updateManageObject(auth.get().internalID, json.dumps(getStats()))
    except Exception as e:
        logger.error('The following error occured: ' + str(e))

def start():
    try:
        while True:
            main()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
        pass

def getStats():
    try:
        rawStats = subprocess.Popen(["docker", "stats", "--no-stream","-a", "--format", "'{{.Container}};{{.Name}};{{.CPUPerc}};{{.MemUsage}}'"],stdout=subprocess.PIPE)
        list = rawStats.stdout.read().decode('utf-8').split('\n')
        #for i in list2:
        #      print(i)
        #list = ["'6e0d6ef04eca;node-red;0.00%;1.82%'", "'1e856c41a0f8;apama;0.21%;1.90%'", "'63058916b21b;zementis;0.11%;15.10%'", "'cc8e915395cd;wm-is;0.17%;17.62%'", "'77409e5fec3c;mosquitto;0.03%;0.01%'", '']
        a = []
        for i in list:
            dict = {}
            for counter,value in enumerate(i.split(';')):
                if counter == 0:
                    dict["containerID"] = value.replace("'","")
                if counter == 1:
                    dict["name"] = value
                    nameString = "name=" + str(value)
                    try:
                        rawStatus = subprocess.Popen(["docker", "ps", "-a", "--format", "'{{.Status}}'", "--filter", nameString ],stdout=subprocess.PIPE)
                        dict["status"] = rawStatus.stdout.read().decode('utf-8').replace("'","")
                    except:
                        logger.warning('Status from docker for container %s not valid.'% (str(value)))
                        dict["status"] = "Unknown"
                if counter == 2:
                    dict["cpu"] = value.replace('%','')
                if counter == 3:
                    dict["memory"] = value.replace('%','').replace("'","")
            a.append(dict)
        a = a[:-1]
        payload = {}
        payload['c8y_Docker'] = a
        logger.debug('The following Docker stats where found: %s'% (str(payload)))
        return payload
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
