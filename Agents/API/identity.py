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
    try:
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
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))
        return False

def getExternalID(internalID):
    logger.info('Checking against indentity service what are the externalID´s for the device ID in C8Y')
    try:
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
                return False
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                        str(response.status_code))
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

def createExternalID(deviceID,internalID,type):
    logger.info('Create an external id for an existing managed object')
    try:
        url = "https://%s/identity/globalIds/%s/externalIds"%(auth.get().tenant, internalID)
        payload = "{\n\t\"externalId\": \"%s\",\n    \"type\": \"%s\"\n}"%(deviceID,type)
        response = requests.request("POST", url, headers=auth.get().headers, data = payload)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Serial nummer entered')
            logger.debug('Receiving the following response %s'%(str(response.text)))
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

if __name__ == '__main__':
    pass
