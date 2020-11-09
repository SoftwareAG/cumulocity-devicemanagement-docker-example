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
    url = "https://%s/inventory/managedObjects/%s"%(auth.get().tenant, internalID)
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Managed object exists in C8Y')
        json_data = json.loads(response.text)
        return json_data
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def updateManageObject(internalID, payload):
    logger.info('Update of managed Object')
    url = "https://%s/inventory/managedObjects/%s"%(auth.get().tenant, internalID)
    response = requests.request("PUT", url, headers=auth.get().headers, data = payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Managed object updated in C8Y')
        return True
    else:
        logger.warning('Managed object not updated in C8Y')
        raise Exception


if __name__ == '__main__':
    pass
