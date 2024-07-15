import paho.mqtt.client as mqtt
import numpy as np
import threading
import datetime
import json
import time

from collections import defaultdict
from dataFilter import kalman_filter as kf
from mosquitto_broker import mqtt_broker
from mosquitto_broker import mqtt_sub

time_form = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
file_path = time_form + '_rssi.json'

# set MQTT broker
broker_address = "192.168.0.71"  # 브로커의 주소
broker_port = 1883  # 브로커의 포트

# set client 
client = mqtt.Client()

# MAC address data dict
mac_data = defaultdict(list)

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

def run_sub(broker_address, broker_port):
    sub = mqtt_sub()
    client.on_connect = sub.sub_connect
    client.on_message = sub.message
    client.connect(broker_address, broker_port)
    client.loop_forever()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
        
def start_sub_delay():
    time.sleep(15)
    run_sub(broker_address, broker_port)

if __name__ == "__main__":
    # 멀티스레드로 각각의 기능을 실행
    mqtt_broker_thread = threading.Thread(target=run_broker)
    mqtt_sub_thread = threading.Thread(target=start_sub_delay)
    
    mqtt_broker_thread.start()
    mqtt_sub_thread.start()

    # 메인 스레드가 종료되기 전까지 대기
    try:
        mqtt_broker_thread.join()
        mqtt_sub_thread.join()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting main thread...")
