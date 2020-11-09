import sys
import utils.settings
import requests
import logging
import json
import API.authentication as auth

logger = logging.getLogger('Identity API')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for identity was initialised')

def getInternalID(externalID):
    logger.info('Checking against indentity service what is internalID in C8Y')
    url = "https://%s/identity/externalIds/c8y_Serial/%s"%(auth.get().tenant, externalID)
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Managed object exists in C8Y')
        json_data = json.loads(response.text)
        internalID = json_data['managedObject']['id']
        logger.info("The interalID for " + str(externalID) + " is " + str(internalID))
        logger.debug('Returning the internalID')
        return internalID
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        return False

def getExternalID(internalID):
    logger.info('Checking against indentity service what are the externalID´s for the device ID in C8Y')
    url = "https://%s/identity/globalIds/%s/externalIds"%(auth.get().tenant, internalID)
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['externalIds']:
            logger.info('Managed object exists in C8Y')
            externalID = {}
            for i in json_data:
                externalID[json_data['externalIds'][i]['type']] = json_data['externalIds'][i]['externalId']
            logger.info("The externalID´s for " + str(internalID) + "are " + str(externalID))
            logger.debug('Returning the externalID')
            return externalID
        else:
            logger.warning('Managed object does not exist in C8Y')
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def createExternalID(deviceID,internalID):
    logger.info('Create an external id for an existing managed object')
    url = "https://%s/identity/globalIds/%s/externalIds"%(auth.get().tenant, internalID)
    payload = "{\n\t\"externalId\": \"%s\",\n    \"type\": \"c8y_Serial\"\n}"%(deviceID)
    response = requests.request("POST", url, headers=auth.get().headers, data = payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Serial nummer entered')
        json_data = json.loads(response.text)
        logger.debug('Receiving the following response %s'%(str(response.text)))
        return True
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        return False

if __name__ == '__main__':
    pass
