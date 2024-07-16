import paho.mqtt.client as mqtt
import numpy as np
import threading
import time

from collections import defaultdict
from mosquitto_broker import mqtt_broker
from mosquitto_broker import mqtt_sub

# set MQTT broker
broker_address = "192.168.22.233" 
broker_port = 1883 

# set client 
client = mqtt.Client()

# MAC address data dict
mac_data = defaultdict(list)

# running mqtt broker
def run_broker():
    broker = mqtt_broker()
    broker.broker_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        broker.terminate()
        print("Broker thread is terminated.")

# running mqtt subcriber
def run_sub(broker_address, broker_port):
    sub = mqtt_sub()
    client.on_connect = sub.sub_connect
    client.on_message = sub.on_message
    client.connect(broker_address, broker_port)
    client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
        
#waiting broker is already
def start_sub_delay():
    time.sleep(5)
    run_sub(broker_address, broker_port)

if __name__ == "__main__":
    # multithreading
    mqtt_broker_thread = threading.Thread(target=run_broker)
    mqtt_sub_thread = threading.Thread(target=start_sub_delay)
    
    mqtt_broker_thread.start()
    mqtt_sub_thread.start()

    # waiting for break
    try:
        mqtt_broker_thread.join()
        mqtt_sub_thread.join()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting main thread...")
