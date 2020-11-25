import requests
import logging
import json
import API.authentication as auth
import API.identity
import sys


logger = logging.getLogger('Inventory API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for Inventory was initialised')

def getSpezificManagedObject(internalID):
    logger.info('Checking for managed object in c8y')
    try:
        url = "https://%s/inventory/managedObjects/%s"%(auth.get().tenant, internalID)
        logger.debug('Requesting the following url: ' + str(url))
        response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Managed object exists in C8Y')
            json_data = json.loads(response.text)
            return json_data
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

def updateManageObject(internalID, payload):
    logger.info('Update of managed Object')
    try:
        url = "https://%s/inventory/managedObjects/%s"%(auth.get().tenant, internalID)
        response = requests.request("PUT", url, headers=auth.get().headers, data = payload)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Managed object updated in C8Y')
            return True
        else:
            logger.warning('Managed object not updated in C8Y')
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


if __name__ == '__main__':
    pass
