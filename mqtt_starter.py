# import paho.mqtt.client as mqtt
# import numpy as np
# import time

# from collections import defaultdict
# from mqtt import mqtt_broker, mqtt_sub 

# # set MQTT broker
# broker_address = "192.168.0.71" 
# broker_port = 1883

# # set client 
# number1_client = mqtt.Client()
# number2_client = mqtt.Client()
# number3_client = mqtt.Client()
# number4_client = mqtt.Client()
# number5_client = mqtt.Client()

# # MAC address data dict
# mac_data = defaultdict(list)

# class run_mqtt():
#     def __init__(self):
#         # set MQTT broker
#         self.broker_address = "192.168.0.71" 
#         self.broker_port = 1883
        
#     # running mqtt broker
#     def run_broker():
#         broker = mqtt_broker()
#         broker.broker_start()

#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             broker.terminate()
#             print("Broker thread is terminated.")
            
#     # running mqtt subcriber
#     def run_number1_sub(self):
#         number1_sub = mqtt_sub()
#         number1_client.on_connect = number1_sub.number1_sub_connect
#         number1_client.on_message = number1_sub.on_message_to_number1
#         number1_client.connect(self.broker_address, self.broker_port)
#         number1_client.loop_forever()
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             print("sub thread is terminated.")
            
#     # waiting for broker is already
#     def start_number1_sub(self):
#         time.sleep(5)
#         self.run_number1_sub
            
#     def run_number2_sub(self):
#         number2_sub = mqtt_sub()
#         number2_client.on_connect = number2_sub.number2_sub_connect
#         number2_client.on_message = number2_sub.on_message_to_number2
#         number2_client.connect(self.broker_address, self.broker_port)
#         number2_client.loop_forever()
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             print("sub thread is terminated.")
        
#     def start_number2_sub(self):
#         time.sleep(5)
#         self.run_number2_sub
        
#     def run_number3_sub(self):
#         number3_sub = mqtt_sub()
#         number3_client.on_connect = number3_sub.number3_sub_connect
#         number3_client.on_message = number3_sub.on_message_to_number3
#         number3_client.connect(self.broker_address, self.broker_port)
#         number3_client.loop_forever()
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             print("sub thread is terminated.")
        
#     def start_number3_sub(self):
#         time.sleep(5)
#         self.run_number3_sub
        
#     def run_number4_sub(self):
#         number4_sub = mqtt_sub()
#         number4_client.on_connect = number4_sub.number4_sub_connect
#         number4_client.on_message = number4_sub.on_message_to_number4
#         number4_client.connect(self.broker_address, self.broker_port)
#         number4_client.loop_forever()
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             print("sub thread is terminated.")
        
#     def start_number4_sub(self):
#         time.sleep(5)
#         self.run_number4_sub
        
#     def run_number5_sub(self):
#         number5_sub = mqtt_sub()
#         number5_client.on_connect = number5_sub.number5_sub_connect
#         number5_client.on_message = number5_sub.on_message_to_number5
#         number5_client.connect(self.broker_address, self.broker_port)
#         number5_client.loop_forever()
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt! Exiting...")
#         finally:
#             print("sub thread is terminated.")
        
#     def start_number5_sub(self):
#         time.sleep(5)
#         self.run_number5_sub