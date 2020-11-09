import sys


def content(name):
    with open('../apama-mqtt-connect/monitors/' + str(name) + '.mon', 'r') as file:
        data = file.read()
        return data
