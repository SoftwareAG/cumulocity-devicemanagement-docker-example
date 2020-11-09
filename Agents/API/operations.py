
import requests
import logging
import json
import API.authentication as auth


logger = logging.getLogger('Operations API')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for operations was initialised')


def setOperationMode(operationID, status, text = ''):
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
        raise Exception
    logger.info('Response from request with code : ' + str(response.status_code))
    if response.status_code == 200:
        logger.info('Operation successfully set to Executing')
        return True
    else:
        logger.error('Operation not successfully set to Executing')
        raise Exception
