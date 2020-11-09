import jsonify
import sys
import csv
import logging
import requests
from os import path
import configparser
from base64 import b64encode
import utils.settings


class __Authentication(object):
    def __init__(self):
        self.logger = logging.getLogger('Authentication')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Logger for authentication was initialised')
        if path.exists('./config/credentials.key'):
            self.configCredentials = configparser.ConfigParser(interpolation=None)
            self.configCredentials.read('./config/credentials.key')
            self.logger.info('Key file was read')
            self.__c8yUser = self.configCredentials['Credentials']['Username']
            self.__c8yPassword = self.configCredentials['Credentials']['Password']
            self.tenantID = self.configCredentials['Credentials']['tenantID']
            self.basicSettings = utils.settings.basics()
            self.tenantInstance = self.basicSettings['tenantInstance']
            self.tenant = self.tenantID + "." + self.tenantInstance
            self.MqttUser = self.tenantID + "/" + self.__c8yUser
            self.MqttPwd = self.__c8yPassword
            self.payload = {}
            self.headers = {"Authorization": "Basic {}".format(b64encode(bytes(self.tenantID + "/" + f"{self.__c8yUser}:{self.__c8yPassword}", "utf-8")).decode("ascii")), 'Content-Type': 'application/json','Accept': 'application/json'}
    instance = None


def get():
    if not __Authentication.instance:
        __Authentication.instance = __Authentication()
    return __Authentication.instance


if __name__ == '__main__':
    pass
