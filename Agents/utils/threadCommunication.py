import jsonify
import sys
import csv
import logging
import requests
from os import path
import configparser
from base64 import b64encode
import utils.settings


class __ThreadCommunication(object):
    def __init__(self):
        self.logger = logging.getLogger('Thread Communication')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Logger for the thread communication was initialised')
        self.queue = {}

    instance = None

    def addTask(self, task, thread):
        self.thread = thread
        self.task = task
        if self.thread not in self.queue:
            self.queue[self.thread] = [self.task]
        else:
            self.queue[self.thread].append(self.task)
        self.logger.info('Added task %s for %s into thread communication'%(str(self.task),str(self.thread)))

    def getTasks(self, thread):
        self.thread = thread
        if self.thread in self.queue:
            return self.queue[self.thread]
        else:
            self.logger.warning('Thread %s does not exist'%(str(self.thread)))
            return None

    def removeTask(self, task, thread):
        self.task = task
        self.thread = thread
        if self.thread in self.queue:
            if self.task in self.queue[self.thread]:
                self.queue[self.thread].remove(self.task)
                return True
            else:
                self.logger.warning('Task %s does not exist'%(str(self.task)))
                return False
        else:
            self.logger.warning('Thread %s does not exist'%(str(self.thread)))
            return False


def getInstance():
    if not __ThreadCommunication.instance:
        __ThreadCommunication.instance = __ThreadCommunication()
    return __ThreadCommunication.instance

def getTasks(thread):
    return getInstance().getTasks(thread)

def addTask(task, thread):
    getInstance().addTask(task, thread)

def removeTask(task, thread):
    getInstance().removeTask(task, thread)

if __name__ == '__main__':
    pass
