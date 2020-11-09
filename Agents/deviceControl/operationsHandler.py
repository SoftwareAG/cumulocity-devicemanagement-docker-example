import API.authentication as auth
import logging
import requests
import json
import API.inventory
from API.device_proxy import DeviceProxy, WebSocketFailureException
import deviceControl.modelExchange
import sys
import os
import utils.settings
import deviceControl.configurationUpdate
import API.operations
import streamingAnalytics.listener
import dockerWatcher.sendDockerStats
import subprocess

logger = logging.getLogger('OperationHandler')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for handling operations was initialised')

def start(internalID, operation):
    logger.debug('Getting the managedObject to check the Supported Operations')
    operationID = operation['id']
    operationClassification(operation, operationID)

def operationClassification(operation, operationID):
    if 'c8y_Restart' in str(operation):
        logger.info('Found c8y_Restart operation')
        API.operations.setOperationMode(operationID, 'EXECUTING')
        API.operations.setOperationMode(operationID, 'SUCCESSFUL')
    elif 'c8y_Configuration' in str(operation):
        logger.info('Found c8y_Configuration operation')
        try:
            deviceControl.configurationUpdate.start(operation, operationID)
            API.operations.setOperationMode(operationID, 'SUCCESSFUL')
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED', str(e))
    elif 'c8y_Command' in str(operation):
        logger.info('Found c8y_Command operation')
        API.operations.setOperationMode(operationID, 'EXECUTING')
        API.operations.setOperationMode(operationID, 'SUCCESSFUL')
    elif 'c8y_RemoteAccessConnect' in str(operation):
        logger.info('Found c8y_RemoteAccessConnect operation')
        API.operations.setOperationMode(operationID, 'EXECUTING')
        connect = operation['c8y_RemoteAccessConnect']
        device_proxy = DeviceProxy(connect['hostname'], connect['port'], None, connect['connectionKey'], auth.get().tenantInstance, auth.get().tenantID, utils.settings.credentials()['c8yUser'],utils.settings.credentials()['c8yPassword'], None)
        try:
            device_proxy.connect()
            API.operations.setOperationMode(operationID, 'SUCCESSFUL')
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED', str(e))
    elif 'c8y_ThinEdge_Model' in str(operation):
        logger.info('Found a c8y_ThinEdge_Model operation')
        try:
            API.operations.setOperationMode(operationID, 'EXECUTING')
            newModel = deviceControl.modelExchange.NewModel(operation['c8y_ThinEdge_Model']['name'], operation['c8y_ThinEdge_Model']['type'], operation['c8y_ThinEdge_Model']['id'],operation['c8y_ThinEdge_Model']['order'])
            newModel.main()
            API.operations.setOperationMode(operationID, 'SUCCESSFUL')
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED', str(e))
    elif 'c8y_Docker' in str(operation):
        logger.info('Found a c8y_Docker operation')
        try:
            API.operations.setOperationMode(operationID, 'EXECUTING')
            if operation['c8y_Docker']['command'] == 'create':
                process = subprocess.Popen(["docker","run","-d","--name",str(operation['c8y_Docker']['options']['name']),"-p",str(operation['c8y_Docker']['options']['ports']),str(operation['c8y_Docker']['options']['image'])],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                #cmd = "docker run -d " + "--name " + str(operation['c8y_Docker']['options']['name']) + " " + str(operation['c8y_Docker']['options']['image'])
            elif operation['c8y_Docker']['command'] == 'delete':
                process = subprocess.Popen(["docker","stop",str(operation['c8y_Docker']['name'])],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                process = subprocess.Popen(["docker","rm",str(operation['c8y_Docker']['name'])],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                #cmd = "docker stop " + str(operation['c8y_Docker']['name']) + "&& docker rm " + str(operation['c8y_Docker']['name'])
            elif operation['c8y_Docker']['command'] == 'restart':
                process = subprocess.Popen(["docker","restart",str(operation['c8y_Docker']['name'])],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #cmd = "docker " + str(operation['c8y_Docker']['command']) + " " + str(operation['c8y_Docker']['name'])
            elif operation['c8y_Docker']['command'] == 'stop':
                process = subprocess.Popen(["docker","stop",str(operation['c8y_Docker']['name'])],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #cmd = "docker " + str(operation['c8y_Docker']['command']) + " " + str(operation['c8y_Docker']['name'])
            elif operation['c8y_Docker']['command'] == 'start':
                process = subprocess.Popen(["docker","start",str(operation['c8y_Docker']['name'])],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #cmd = "docker " + str(operation['c8y_Docker']['command']) + " " + str(operation['c8y_Docker']['name'])
            process.wait()
            if process.returncode == 0:
                API.operations.setOperationMode(operationID, 'SUCCESSFUL')
            else:
                stderr = str(process.stderr.read().decode('utf-8'))
                logger.error('Following error raised for docker:%s'%str(stderr))
                API.operations.setOperationMode(operationID = operationID, status = 'FAILED', text = stderr)
        except Exception as e:
            logger.error('The following error occured: %s'%(str(e)))
            API.operations.setOperationMode(operationID, 'FAILED', str(e))
    else:
        logger.warning('Unknown operation type')
