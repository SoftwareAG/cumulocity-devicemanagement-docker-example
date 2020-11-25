
import requests
import logging
import json
import API.authentication as auth
import deviceControl.operationsHandler
import threading


logger = logging.getLogger('Operations API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for operations was initialised')


def setOperationMode(operationID, status, text = ''):
    try:
        mode = status
        url = "https://%s/devicecontrol/operations/%s"%(auth.get().tenant, operationID)
        if mode == 'EXECUTING' or 'SUCCESSFUL' or 'FAILED':
            logger.info('Operation ' + str(mode))
            data = {}
            data['status'] = str(status)
            if mode == 'FAILED':
                data['failureReason'] = str(text)
            response = requests.request("PUT", url, headers=auth.get().headers, data = json.dumps(data))
        else:
            logger.error('Mode not known')
            return False
        logger.info('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200:
            logger.info('Operation successfully set to Executing')
            return True
        else:
            logger.error('Operation not successfully set to Executing')
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

def getPendingOperations(internalID):
    try:
        url = "https://%s/devicecontrol/operations?status=PENDING&deviceId=%s"%(auth.get().tenant, internalID)
        response = requests.request("GET", url, headers=auth.get().headers, data = auth.get().payload)
        logger.info('Response from request: ' + str(response.text))
        logger.info('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200:
            logger.info('Valid request')
            json_data = json.loads(response.text)
            logger.debug('Json response: %s'%(str(json_data)))
            logger.info('Checking if operations is not empty')
            if not json_data['operations']:
                logger.debug('Operations is empty, returns False')
                return False
            logger.info('Operation is not empty')
            logger.debug('Looping through operations')
            for operation in json_data['operations']:
                logger.debug('Current item: %s'%(str(operation)))
                operationsHandlerThread = threading.Thread(target=deviceControl.operationsHandler.start, kwargs=dict(internalID=auth.get().internalID,operation=operation ), daemon=True)
                operationsHandlerThread.start()
        else:
            logger.warning('Got response with status_code: ' + str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))

