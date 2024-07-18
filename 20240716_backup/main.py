import paho.mqtt.client as mqtt
import numpy as np
import threading
import time

from collections import defaultdict
from mqtt import mqtt_broker, mqtt_sub 

# set MQTT broker
broker_address = "192.168.0.71" 
broker_port = 1883

# set client 
main_client = mqtt.Client()
meetingroom_client = mqtt.Client()

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
def run_main_sub(broker_address, broker_port):
    main_sub = mqtt_sub()
    main_client.on_connect = main_sub.main_sub_connect
    main_client.on_message = main_sub.on_message_to_main
    main_client.connect(broker_address, broker_port)
    main_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
        
def run_meetingroom_sub(broker_address, broker_port):
    meetingroom_sub = mqtt_sub()
    meetingroom_client.on_connect = meetingroom_sub.meetingroom_sub_connect
    meetingroom_client.on_message = meetingroom_sub.on_message_to_meetingroom
    meetingroom_client.connect(broker_address, broker_port)
    meetingroom_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
        
#waiting broker is already
def start_main_sub_delay():
    time.sleep(5)
    run_main_sub(broker_address, broker_port)
            
#waiting broker is already
def start_meetingroom_sub_delay():
    time.sleep(5)
    run_meetingroom_sub(broker_address, broker_port)

if __name__ == "__main__":
    # multithreading
    mqtt_broker_thread = threading.Thread(target=run_broker)
    mqtt_main_sub_thread = threading.Thread(target=start_main_sub_delay)
    mqtt_meetingroom_sub_thread = threading.Thread(target=start_meetingroom_sub_delay)
    
    mqtt_broker_thread.start()
    mqtt_main_sub_thread.start()
    mqtt_meetingroom_sub_thread.start()
    
    # waiting for break
    try:
        mqtt_broker_thread.join()
        mqtt_main_sub_thread.join()
        mqtt_meetingroom_sub_thread.join()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting main thread...")
