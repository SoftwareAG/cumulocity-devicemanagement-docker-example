import requests
import logging
import json
import API.authentication as auth
from datetime import datetime, date, time, timedelta


logger = logging.getLogger('Event API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for Events was initialised')

def getEventsFromManagedObject(internalID, pageSize=2500, days=0, currentPage=1):
    logger.info('Checking for events of managed object in c8y')
    if days != 0:
        dateFrom = date.today()
        dateTo = date.today() - timedelta(days)
        url = "https://%s/event/events?pageSize=%s&source=%s&dateFrom=%s&dateTo=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, internalID, dateFrom, dateTo, currentPage, )
    else:
        url = "https://%s/event/events?pageSize=%s&source=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, internalID, currentPage, )
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Received events')
        json_data = json.loads(response.text)
        logger.debug('Receiving the following response %s'%(str(response.text)))
        return json_data
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def getEvents(pageSize=2500, days=0, currentPage=1):
    logger.info('Checking for events in c8y')
    if days != 0:
        dateFrom = date.today()
        dateTo = date.today() - timedelta(days)
        url = "https://%s/event/events?pageSize=%s&dateFrom=%s&dateTo=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, dateFrom, dateTo, currentPage, )
    else:
        url = "https://%s/event/events?pageSize=%s&currentPage=%s&withTotalPages=True"%(auth.get().tenant, pageSize, currentPage, )
    logger.debug('Requesting the following url: ' + str(url))
    response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
    logger.debug('Response from request: ' + str(response.text))
    logger.debug('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Received events')
        json_data = json.loads(response.text)
        return json_data
    else:
        logger.error('Receiving following status code %s'%(str(response.status_code)))
        raise Exception

def createEvent(type, text, source ):
    logger.info('Creating event in c8y')
