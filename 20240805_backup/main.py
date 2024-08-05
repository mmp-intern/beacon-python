import paho.mqtt.client as mqtt
import multiprocessing
import time

from collections import defaultdict
from mqtt import mqtt_broker, mqtt_sub 
from fix_wrong_json import handling_json_file

# set MQTT broker
broker_address = "192.168.0.71" 
broker_port = 1883

# set client 
number1_client = mqtt.Client()
number2_client = mqtt.Client()
number3_client = mqtt.Client()
number4_client = mqtt.Client()
number5_client = mqtt.Client()

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
def run_number1_sub(broker_address, broker_port):
    connected = False
    number1_sub = mqtt_sub()
    number1_client.on_connect = number1_sub.number1_sub_connect
    number1_client.on_message = number1_sub.on_message_to_number1
    number1_client.connect(broker_address, broker_port)
    number1_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
    
        
# waiting for broker is already
def start_number1_sub_delay():
    time.sleep(5)
    run_number1_sub(broker_address, broker_port)
        
def run_number2_sub(broker_address, broker_port):
    number2_sub = mqtt_sub()
    number2_client.on_connect = number2_sub.number2_sub_connect
    number2_client.on_message = number2_sub.on_message_to_number2
    number2_client.connect(broker_address, broker_port)
    number2_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
    
def start_number2_sub_delay():
    time.sleep(5)
    run_number2_sub(broker_address, broker_port)
    
def run_number3_sub(broker_address, broker_port):
    number3_sub = mqtt_sub()
    number3_client.on_connect = number3_sub.number3_sub_connect
    number3_client.on_message = number3_sub.on_message_to_number3
    number3_client.connect(broker_address, broker_port)
    number3_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
    
def start_number3_sub_delay():
    time.sleep(5)
    run_number3_sub(broker_address, broker_port)
    
def run_number4_sub(broker_address, broker_port):
    number4_sub = mqtt_sub()
    number4_client.on_connect = number4_sub.number4_sub_connect
    number4_client.on_message = number4_sub.on_message_to_number4
    number4_client.connect(broker_address, broker_port)
    number4_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
    
def start_number4_sub_delay():
    time.sleep(5)
    run_number4_sub(broker_address, broker_port)
    
def run_number5_sub(broker_address, broker_port):
    number5_sub = mqtt_sub()
    number5_client.on_connect = number5_sub.number5_sub_connect
    number5_client.on_message = number5_sub.on_message_to_number5
    number5_client.connect(broker_address, broker_port)
    number5_client.loop_forever()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting...")
    finally:
        print("sub thread is terminated.")
    
def start_number5_sub_delay():
    time.sleep(5)
    run_number5_sub(broker_address, broker_port)
    
if __name__ == "__main__":
    # Multiprocessing
    mqtt_broker_process = multiprocessing.Process(target=run_broker)
    mqtt_number1_sub_process = multiprocessing.Process(target=start_number1_sub_delay)
    mqtt_number2_sub_process = multiprocessing.Process(target=start_number2_sub_delay)
    mqtt_number3_sub_process = multiprocessing.Process(target=start_number3_sub_delay)
    mqtt_number4_sub_process = multiprocessing.Process(target=start_number4_sub_delay)
    mqtt_number5_sub_process = multiprocessing.Process(target=start_number5_sub_delay)
    test = handling_json_file()
    
    # Starting processes
    mqtt_broker_process.start()
    mqtt_number1_sub_process.start()
    mqtt_number2_sub_process.start()
    mqtt_number3_sub_process.start()
    mqtt_number4_sub_process.start()
    mqtt_number5_sub_process.start()
    while(1):
        test.combine_json_files()
        
        
    # Waiting for processes to finish
    try:
        mqtt_broker_process.join()
        mqtt_number1_sub_process.join()
        mqtt_number2_sub_process.join()
        mqtt_number3_sub_process.join()
        mqtt_number4_sub_process.join()
        mqtt_number5_sub_process.join()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt! Exiting main process...")
