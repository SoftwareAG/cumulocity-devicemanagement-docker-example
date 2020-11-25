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
    if path.exists('./config/config.ini'):
        configInit = configparser.ConfigParser(interpolation=None)
        configInit.read('./config/config.ini')
        basics = {}
        basics['tenantInstance'] = configInit['C8Y']['tenantInstance']
        basics['registrationUser'] = configInit['Registration']['user']
        basics['registrationPassword'] = configInit['Registration']['password']
        basics['registrationTenant'] = configInit['Registration']['tenant']
        basics['deviceID'] = configInit['Device']['id']
        basics['tenantPostFix'] = configInit['Registration']['tenantPostFix']
        logger.debug('Returning the basics object: %s'%(str(basics)))
        return basics
    else:
        logger.error('There is no config file, returning False')
        return False

def credentials():
    logger.info('Credentials function was called, checking if file exists')
    if path.exists('./config/credentials.key'):
        logger.info('Credential key file exists')
        configCredentials = configparser.ConfigParser(interpolation=None)
        configCredentials.read('./config/credentials.key')
        logger.info('Key file was read')
        credentials = {}
        credentials['c8yUser'] = configCredentials['Credentials']['Username']
        logger.debug('Following user was found in key file: ' + str(credentials['c8yUser']))
        credentials['tenantID'] = configCredentials['Credentials']['tenantID']
        logger.debug('Following user was found in key file: ' + str(credentials['tenantID']))
        credentials['c8yPassword'] = configCredentials['Credentials']['Password']
        logger.debug('Returning the credentials object: %s'%(str(credentials)))
        return credentials
    else:
        logger.error('There is no credentials.key file, returning False')
        return False

def mqtt():
    if path.exists('./config/credentials.key'):
        configInit = configparser.ConfigParser(interpolation=None)
        configInit.read('./config/config.ini')
        mqtt = {}
        mqtt['prefix'] = configInit['MQTT']['prefix']
        mqtt['prefixSignaltype'] = configInit['MQTT']['prefixSignaltype']
        mqtt['broker'] = configInit['MQTT']['broker']
        mqtt['port'] = configInit['MQTT']['port']
        logger.debug('Returning the mqtt settings: %s'%(str(mqtt)))
        return mqtt
    else:
        logger.error('There is no config file, returning False')
        return False

def device():
    device ={}
    try:
        managedDeviceObject = API.inventory.getSpezificManagedObject(auth.get().internalID)['c8y_Configuration']['config'].replace('\n','').split(';')
        for counter, value in enumerate(managedDeviceObject):
            if len(value) > 0:
                device[str(value.split('=')[0])] = value.split('=')[1]
            else:
                pass
        return device
    except Exception as e:
        logger.error('The following error occured: %s'% (str(e)))
        return device
