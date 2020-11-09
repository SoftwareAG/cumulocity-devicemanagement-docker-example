import configparser
from os import path
import logging
import os
import API.inventory
import API.epl
import API.authentication as auth

logger = logging.getLogger('Settings')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info('Logger for settings was initialised')

def basics():
    logger.info('Basic function was called')
    configInit = configparser.ConfigParser(interpolation=None)
    configInit.read('./config/config.ini')
    basics = {}
    basics['tenantInstance'] = configInit['C8Y']['tenantInstance']
    basics['registrationUser'] = configInit['Registration']['user']
    basics['registrationPassword'] = configInit['Registration']['password']
    basics['registrationTenant'] = configInit['Registration']['tenant']
    basics['deviceID'] = configInit['Device']['id']
    basics['tenantPostFix'] = configInit['Registration']['tenantPostFix']
    return basics

def credentials():
    logger.info('Credentials function was called, checking if file exists')
    if path.exists('./config/credentials.key'):
        logger.info('Credential key file exists')
        configInit = configparser.ConfigParser(interpolation=None)
        configCredentials.read('./config/credentials.key')
        logger.info('Key file was read')
        credentials = {}
        credentials['c8yUser'] = configCredentials['Credentials']['Username']
        logger.debug('Following user was found in key file: ' + str(credentials['c8yUser']))
        credentials['tenantID'] = configCredentials['Credentials']['tenantID']
        logger.debug('Following user was found in key file: ' + str(credentials['tenantID']))
        credentials['c8yPassword'] = configCredentials['Credentials']['Password']
        return credentials
    else:
        print("No file")

def mqtt():
    configInit = configparser.ConfigParser(interpolation=None)
    configInit.read('./config/config.ini')
    mqtt = {}
    mqtt['prefix'] = configInit['MQTT']['prefix']
    mqtt['prefixSignaltype'] = configInit['MQTT']['prefixSignaltype']
    mqtt['broker'] = configInit['MQTT']['broker']
    mqtt['port'] = configInit['MQTT']['port']
    return mqtt

def device():
    device = {}
    managedDeviceObject = API.inventory.getSpezificManagedObject(auth.get().internalID)['c8y_Configuration']['config'].replace('\n','').split(';')
    for counter, value in enumerate(managedDeviceObject):
        if len(value) > 0:
            device[str(value.split('=')[0])] = value.split('=')[1]
        else:
            pass
    return device
