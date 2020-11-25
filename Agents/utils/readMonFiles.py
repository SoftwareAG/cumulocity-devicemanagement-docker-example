import sys


def content(name):
    try:
        with open('../apama-mqtt-connect/monitors/' + str(name) + '.mon', 'r') as file:
            data = file.read()
            return data
    except:
        return []
