
import requests
import logging
import json
import API.authentication as auth


logger = logging.getLogger('EPL API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for EPL was initialised')


def getModel(id):
    url = "https://%s/service/cep/analyticsbuilder/%s"%(auth.get().tenant,id)
    response = requests.request("GET", url, headers=auth.get().headers)
    logger.debug('Response from request with code : %s'%(str(response.status_code)))
    if response.status_code == 200:
        logger.debug('Following responds text: ' + str(response.text))
        json_data = json.loads(response.text)
        return json_data
    else:
        logger.error('Raising exception')
        raise Exception

def getModels():
    url = "https://%s/service/cep/analyticsbuilder"%(auth.get().tenant)
    response = requests.request("GET", url, headers=auth.get().headers)
    logger.debug('Response from request with code : %s'%(str(response.status_code)))
    if response.status_code == 200:
        logger.debug('Following responds text: ' + str(response.text))
        json_data = json.loads(response.text)
        return json_data
    else:
        logger.error('Raising exception')
        raise Exception

def createModels(payload):
    print(payload)
    url = "https://%s/service/cep/analyticsbuilder"%(auth.get().tenant)
    print(url)
    response = requests.request("POST", url, headers=auth.get().headers, data=payload)
    print(response.text)
    print(response.status_code)
    logger.debug('Response from request with code : %s'%(str(response.status_code)))
    if response.status_code == 201:
        logger.debug('Following responds text: ' + str(response.text))
        return True
    else:
        logger.error('Raising exception')
        raise Exception
