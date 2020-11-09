import requests
import sys
import logging
import json
from base64 import b64encode
import time
import utils.settings
import API.authentication as auth
import API.identity


logger = logging.getLogger('Device Registration API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for device registration was initialised')


def getDeviceCredentials(id):
    logger.info('Checking for managed object in c8y')
    basicSettings = utils.settings.basics()
    __c8yRegistrationUser = basicSettings['registrationUser']
    __c8yRegistrationPassword = basicSettings['registrationPassword']
    url = "https://%s.%s%s"%(basicSettings['registrationTenant'], basicSettings['tenantInstance'], basicSettings['tenantPostFix'])
    payload = {}
    payload['id'] = id
    headers = {"Authorization": "Basic {}".format(b64encode(bytes(f"{__c8yRegistrationUser}:{__c8yRegistrationPassword}", "utf-8")).decode("ascii")), 'Content-Type': 'application/json','Accept': 'application/json'}
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 201:
        logger.info('Managed object created')
        json_data = json.loads(response.text)
        logger.debug('Returning the managed Object')
        return json_data
    elif response.status_code == 404:
        logger.info(str(response.text))
        if 'PENDING_ACCEPTANCE' in json.loads(response.text):
            logger.info('Device registration awaits acceptance in Tenant.')
        logger.debug('Returning False until Device was accepted in Tenant')
        return False
    else:
        logger.debug('Got response with status_code: ' + str(response.status_code))
        logger.debug(str(response.text))
        logger.debug('Returning False')
        return False

def createEdgeDevice(externalID):
    logger.info('Checking for managed object in c8y with external ID %s' + externalID)
    url = "https://%s/inventory/managedObjects"%(auth.get().tenant)
    with open('./config/device.txt') as f:
        payload = f.read()
    payload = json.loads(payload)
    payload['name'] = "Gateway_%s"%(externalID)
    response = requests.request("POST", url, headers=auth.get().headers, data = json.dumps(payload))
    logger.debug('Requesting the following url: ' + str(url))
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200 or 201:
        logger.info('Device created')
        json_data = json.loads(response.text)
        API.identity.createExternalID(utils.settings.basics()['deviceID'],json_data['id'])
        logger.debug('Returning the managed Object')
        return True
    else:
        logger.warning('Response from request: ' + str(response.text))
        logger.warning('Got response with status_code: ' + str(response.status_code))
        return False
