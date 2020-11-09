import jsonify
import sys
import csv
import logging
import requests
from os import path
from base64 import b64encode
import utils.settings


class __ThreadCommunication(object):
    def __init__(self):
        self.logger = logging.getLogger('Thread Communication')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Logger for the thread communication was initialised')
        self.queue = {}

    instance = None

    def addParticipants(self, thread):
        pass

    def getParticipants(self):
        pass

    def addTask(self, task, thread):
        pass

    def getTask(self):
        pass

    def getSpecificTask(self, thread):
        pass


def get():
    if not __ThreadCommunication.instance:
        __ThreadCommunication.instance = __ThreadCommunication()
    return __ThreadCommunication.instance

def put(value):
    test = get()
    print(test.queue)
    test.queue['Test'] = value
    print(test.queue)



if __name__ == '__main__':
    pass
