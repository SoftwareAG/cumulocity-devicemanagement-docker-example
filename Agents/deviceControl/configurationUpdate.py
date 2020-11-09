import sys
import API.inventory
import requests
import API.operations
import API.authentication as auth
import json
import logging

logger = logging.getLogger('configuration Updater')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def start(operation, operationID):
    API.operations.setOperationMode(operationID, 'EXECUTING')
    configEvent = {}
    configEvent['c8y_Configuration'] = operation['c8y_Configuration']
    try:
        logger.debug('Created the following config: %s'% (str(configEvent)))
        API.inventory.updateManageObject(auth.get().internalID, json.dumps(configEvent))
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
