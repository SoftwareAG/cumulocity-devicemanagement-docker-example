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

def compare(a,b):
    main_list = list(set(b) - set(a))
    return main_list

def models():
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

def update(name):
    payload = {}
    payload['name'] = name
    payload['contents'] = utils.readMonFiles.content(name)
    payload['state'] = "active"
    payload['description'] = ""
    API.epl.createModels(json.dumps(payload))
