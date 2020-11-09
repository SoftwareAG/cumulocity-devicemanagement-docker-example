import requests
import logging
import json
import API.authentication as auth
import API.identity
import sys


logger = logging.getLogger('Binary API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for Inventory was initialised')


def getBinary(binaryID, name):
    logger.info('Getting binary in c8y')
    url = "https://%s/inventory/binaries/%s"%(auth.get().tenant, binaryID)
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Managed object exists in C8Y')
        try:
            file = './binary/' + str(name)
            with open(file, "wb") as code:
                code.write(response.content)
        except Exception as e:
            logger.error('Writing to disc failed due to: ' + str(e))
        logger.debug('File written')
        logger.debug('Returning True')
        return True
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception


if __name__ == '__main__':
    pass
