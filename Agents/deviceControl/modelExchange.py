import requests
import logging
import json
import API.authentication as auth
import API.binary
import os
from datetime import datetime, date, time, timedelta
import paho.mqtt.client as paho
import utils.mqtt





class NewModel(object):

    def __init__(self, name, type, id, order):
        self.logger = logging.getLogger('New Model')
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.info('Logger for an Model exchange was initialised')
        self.name = name
        self.id = id
        self.type = type
        self.order = order
        self.setSettings()

    def setSettings(self):
        if self.type == 'EPL':
            self.path = "../apama-mqtt-connect/monitors/"
            self.suffix = ".mon"
            self.topic = "/model/d/epl"
            self.url = "https://%s/service/cep/eplfiles/%s"%(auth.get().tenant, self.id)
            self.fileContentPrefix = ''
            self.fileContentPostfix = ''
        elif self.type == 'AnalyticsBuilder':
            self.path = "../apama-mqtt-connect/events/"
            self.suffix = ".evt"
            self.topic = "/model/d/ab"
            self.url = "https://%s/service/cep/analyticsbuilder/%s"%(auth.get().tenant, self.id)
            self.fileContentPrefix = "ModelCommand(\"\",\"modelCommands\",\"PUT\",\"/service/cep/analyticsbuilder/%s\",any(string,\""%(self.id)
            self.fileContentPostfix = "\"))"
        elif self.type == 'PMML':
            self.path = "./Models/PMML/"
            self.suffix = ".pmml"
            self.topic = "/model/d/PMML"
            self.url = "https://%s/service/zementis/model/%s"%(auth.get().tenant, self.id)
        elif self.type == 'ONNX':
            self.path = "./Models/ONNX/"
            self.suffix = ".onnx"
            self.topic = "/model/d/ONNX"
            self.url = "https://%s/service/zementis/model/%s"%(auth.get().tenant, self.id)
        self.file = str(self.path) + str(self.name) + str(self.suffix)

    def writeFile(self):
        self.logger.debug('Writing file to disc')
        if self.order == 'load':
            try:
                with open(self.file, "w") as code:
                    code.write(self.fileContent)
                self.logger.debug('SUCCESSFUL write file')
            except Exception as e:
                self.logger.error('The following error occured: %s'%(str(e)))
        if self.order == 'delete':
            try:
                cmd = "rm %s%s%s"%(self.path,self.name,self.suffix)
                os.system(cmd)
                self.logger.debug('SUCCESSFUL deleted file')
            except Exception as e:
                self.logger.error('The following error occured: %s'%(str(e)))


    def getModel(self):
        self.response = requests.request("GET", self.url, headers=auth.get().headers, data = auth.get().payload)
        self.logger.debug('Response from request with code : ' + str(self.response.status_code))
        if self.response.status_code == 200:
            self.logger.debug('Following responds text: ' + str(self.response.text))
            self.json_data = json.loads(self.response.text)
            return self.json_data
        else:
            self.logger.error('Raising exception')
            raise Exception

    def parseContent(self, content):
        self.content = content
        if self.type == 'EPL':
            self.fileContent = self.content['contents']
        elif self.type == 'AnalyticsBuilder':
            self.fileContent = str(self.fileContentPrefix) + json.dumps(self.fileContent).replace("'","\"").replace("\"","\\\"") + str(self.fileContentPostfix)
        elif self.type == 'PMML':
            self.fileContent = self.content
        elif self.type == 'ONNX':
            self.fileContent = self.content
        self.logger.debug(self.fileContent)

    def publishFileExchange(self):
        self.logger.info("Publishing the info about a new model on: " + str(self.topic))
        utils.mqtt.mqttSend(str(self.topic), str(self.name)+ str(self.suffix))

    def injectContentApamaRest(self):
        self.logger.info('Injecting content into Apama Standalone via Rest')
        self.apamaurl = "http://localhost:15903/correlator/code/inject"
        self.headers = {'Content-Type': 'text/plain'}
        self.response = requests.request("PUT", self.apamaurl, headers=self.headers, data = self.fileContent)
        self.logger.debug('Following responds text: ' + str(self.response.text))

    def injectContentApamaCmd(self):
        self.logger.info('Injecting content into Apama Standalone via cmd line')
        if self.order == 'delete' and self.type == 'EPL':
            cmd = "docker exec apama engine_delete %s"%(self.name)
        elif self.order == 'delete' and self.type == 'AnalyticsBuilder':
            cmd = "docker exec apama engine_send %s"%(self.name)
        elif self.order == 'load' and self.type == 'EPL':
            cmd = "docker exec apama engine_inject Project_deployed/monitors/%s%s"%(self.name,self.suffix)
        elif self.order == 'load' and self.type == 'AnalyticsBuilder':
            cmd = "docker exec apama engine_send Project_deployed/events/%s%s"%(self.name,self.suffix)
        os.system(cmd)

    def main(self):
        self.parseContent(self.getModel())
        self.writeFile()
        self.injectContentApamaCmd()
