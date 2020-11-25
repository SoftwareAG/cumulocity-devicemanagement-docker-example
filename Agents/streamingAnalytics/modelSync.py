import configparser
from os import path
import logging
import os
import API.inventory
import API.epl
import API.authentication as auth
import utils.readMonFiles
import json
import subprocess

logger = logging.getLogger('Model Sync')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for modelSync was initialised')


def compare(a,b):
    main_list = list(set(b) - set(a))
    return main_list

def models():
    try:
        models = {}
        models = API.epl.getModels()
        rawStats = subprocess.Popen(["docker", "exec", "apama", "ls", "Project_deployed/monitors"],stdout=subprocess.PIPE)
        rawStats.wait()
        list = rawStats.stdout.read().decode('utf-8').replace('\n','').split('.mon')
        #list = ['ModelManager', 'MyNewAnalyticsModel', 'ReceiveMQTTRawAndRouteC8YMeasurement', '']
        list = list[:-1]
        eplfilelocal = []
        for i in models['eplfiles']:
            for counter,value in enumerate(i):
                if value == 'name':
                    eplfilelocal.append(i[value])
        for i in compare(eplfilelocal,list):
            update(i)
    except Exception as e:
        logger.error('The following error occured: ' + str(e))

def update(name):
    try:
        payload = {}
        payload['name'] = name
        payload['contents'] = utils.readMonFiles.content(name)
        payload['state'] = "active"
        payload['description'] = ""
        API.epl.createModels(json.dumps(payload))
    except Exception as e:
        logger.error('The following error occured: ' + str(e))
