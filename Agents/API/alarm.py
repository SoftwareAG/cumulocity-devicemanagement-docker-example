import requests
import logging
import json
import API.authentication as auth
from datetime import datetime, date, time, timedelta


logger = logging.getLogger('Alarm API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for Alarm was initialised')


def getAlarmsFromManagedObject(internalID, pageSize=2500, days=0, currentPage=1):
    logger.info('Checking for alarms of managed object in c8y')
    if days != 0:
        dateFrom = date.today()
        dateTo = date.today() - timedelta(days)
        url = "https://%s/alarm/alarms?pageSize=%s&source=%s&dateFrom=%s&dateTo=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, internalID, dateFrom, dateTo, currentPage, )
    else:
        url = "https://%s/alarm/alarms?pageSize=%s&source=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, internalID, currentPage, )
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Received alarms')
        json_data = json.loads(response.text)
        return json_data
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def getAlarms(pageSize=2500, days=0, currentPage=1):
    logger.info('Checking for alarms in c8y')
    if days != 0:
        dateFrom = date.today()
        dateTo = date.today() - timedelta(days)
        url = "https://%s/alarm/alarms?pageSize=%s&dateFrom=%s&dateTo=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, dateFrom, dateTo, currentPage, )
    else:
        url = "https://%s/alarm/alarms?pageSize=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, currentPage, )
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Received alarms')
        json_data = json.loads(response.text)
        logger.debug('Receiving the following response %s'%(str(response.text)))
        return json_data
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def createAlarms(type, text, source ):
    logger.info('Creating alarm in c8y')


if __name__ == '__main__':
    pass
