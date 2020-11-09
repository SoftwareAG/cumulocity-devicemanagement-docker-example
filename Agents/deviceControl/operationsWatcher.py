import API.authentication as auth
import logging
import requests
import json
import time
import sys
import threading
import deviceControl.operationsHandler
import API.identity
import utils.settings

logger = logging.getLogger('OperationWatcher')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for watching operations was initialised')

def checkPendingOperations(internalID):
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

def start():
    try:
        while True:
            checkPendingOperations(auth.get().internalID)
            time.sleep(5)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
        pass
