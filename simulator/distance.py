import os
import time
import paho.mqtt.client as paho
import random

if __name__ == '__main__':
    try:
        client = paho.Client()
        client.connect('localhost', 1883, 60)
        while True:
            distance = random.uniform(1, 100)
            if(distance > -1):
                client.publish("raw/Position1/distance", str(distance))
                #print("Measured Distance = %.1f cm" % distance)
            else:
                print("#")
            time.sleep(0.1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
