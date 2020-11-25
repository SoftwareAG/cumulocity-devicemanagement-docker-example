import requests
import sys
import logging
import json
from base64 import b64encode
import time
import utils.settings
import API.authentication as auth
import API.identity


logger = logging.getLogger('SmartRest Template creation logger')
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for SmartRest Template creation was initialized')

def checkSmartRestTemplateExists():
    try:
        logger.info('Checking against indentity service')
        url = "https://%s/identity/externalIds/c8y_SmartRest2DeviceIdentifier/c8y_ThinEdge" % (auth.get().tenant)
        response = requests.request(
            "GET", url, headers=auth.get().headers)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' +
                    str(response.status_code))
        if response.status_code == 404:
            logger.info('SmartRule does not exist in C8Y')
            createSmartRestTemplate()
        else:
            logger.debug('Skippung because SmartRest Template exist')
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

def createSmartRestTemplate():
    try:
        url = "https://%s/inventory/managedObjects" % (auth.get().tenant)
        with open('./config/smartRestTemplate.json') as f:
            payload = f.read()
        payload = json.loads(payload)
        response = requests.request("POST", url, headers=auth.get().headers, data=json.dumps(payload))
        logger.debug('Requesting the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code==201:
            logger.info('Device created')
            json_data = json.loads(response.text)
            API.identity.createExternalID("c8y_ThinEdge", json_data['id'], "c8y_SmartRest2DeviceIdentifier")
            logger.debug('Returning the managed Object')
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                        str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))
