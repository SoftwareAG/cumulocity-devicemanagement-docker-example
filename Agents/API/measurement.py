import requests
import logging
import json
import API.authentication as auth
import sys
from datetime import datetime, date, time, timedelta


logger = logging.getLogger('Measurement API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for Measurements was initialised')


def createMeasurement(payload):
    logger.info('Creating measurements in c8y')
    url = "https://%s/measurement/measurements"%(auth.get().tenant)
    response = requests.request("POST", url, headers=auth.get().headers, data = payload)
    logger.debug('Sending data to the following url: ' + str(url))
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200 or 201:
        logger.info('Measurment send')
        return True
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception


if __name__ == '__main__':
    pass
