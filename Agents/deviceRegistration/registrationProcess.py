
import sys
import time
import logging
import deviceRegistration.newDeviceRegistration
import utils.settings
import API.authentication as auth
import API.identity


logger = logging.getLogger('Device Registration')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for device registration process was initialised')

def start():
    logger.info('Starting the device registration process')
    logger.info('Process yet not successfully finished')
    registrationProcessSuccessfull = False
    logger.info('Process yet not successfully finished')
    basicSettings = utils.settings.basics()
    registrationID = basicSettings['deviceID']
    while not registrationProcessSuccessfull:
        logger.info('Waiting for registration request...')
        logger.info('Registration request with id ' + str(registrationID))
        credentials = deviceRegistration.newDeviceRegistration.getDeviceCredentials(registrationID)
        logger.debug('Received following message : ' + str(credentials))
        if credentials:
            f= open("./config/credentials.key","w+")
            logger.info('Registration was successfully, receiving device credentials.')
            deviceUsername = credentials['username']
            f.write("[Credentials]\r\n")
            f.write("Username =  %s\r\n" % (deviceUsername))
            logger.debug('Username: ' + str(deviceUsername))
            devicePassword = credentials['password']
            f.write("Password =  %s\r\n" % (devicePassword))
            logger.debug('Password: ' + str(devicePassword))
            deviceTenantID = credentials['tenantId']
            f.write("tenantID =  %s\r\n" % (deviceTenantID))
            logger.debug('TenantID: ' + str(deviceTenantID))
            logger.info('Registration was successfully, credentials received, quitting registration process.')
            deviceID = credentials['id']
            logger.debug('Device ID is: ' + str(deviceID))
            f.close
            registrationProcessSuccessfull = True
        time.sleep(5)
    return True
