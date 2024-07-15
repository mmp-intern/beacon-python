import threading
import json
import time
import paho.mqtt.client as mqtt
from collections import defaultdict
from dataFilter import kalman_filter as kf  # dataFilter.py의 kalman_filter 클래스 import
from mosquitto_test import start, terminate, isProcessIDValid, main

# MQTT Broker 정보
broker = "mqtt.eclipse.org"
port = 1883
topic = "/gw/ac233fc18bf0/status"

class mqtt_broker():
    def __init__(self):
        self.mac_data = defaultdict(list)
        self.filter_instance = kf()  # kalman_filter 클래스 인스턴스 생성

    # connect event
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # connect success than subscribing
        client.subscribe("/gw/ac233fc18bf0/status")  # sub topic
        
    # message load
    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        for item in data:
            if "timestamp" in item and "mac" in item and "rssi" in item and 'ibeaconTxPower' in item:
                self.mac_data[item["mac"]].append({
                    "timestamp": item["timestamp"],
                    "mac": item["mac"],
                    "rssi": item["rssi"],
                    "ibeaconTxPower": item["ibeaconTxPower"]
                })

        # Kalman 필터 적용
        for mac, readings in self.mac_data.items():
            rssi_values = [reading['rssi'] for reading in readings]
            filtered_rssi = self.filter_instance.apply_kalman_filter_to_data(rssi_values)
            for i, entry in enumerate(readings):
                entry['rssi_filtered'] = filtered_rssi[i]  # 필터링된 값을 추가

        # 필터링된 결과를 저장하거나 추가적인 처리를 수행할 수 있음
        with open('filtered_data.json', 'w') as json_file:
            json.dump(self.mac_data, json_file, indent=4)

        print("Filtered data saved to 'filtered_data.json'")

# Publish하는 함수
def publish_message(client, topic):
    msg_count = 0
    while True:
        message = f"Hello MQTT {msg_count}"
        client.publish(topic, message)
        print(f"Published: {message}")
        msg_count += 1
        time.sleep(1)

# Subscribe하는 함수
def subscribe_messages(client, topic, broker_instance):
    client.on_connect = broker_instance.on_connect
    client.on_message = broker_instance.on_message
    client.connect(broker, port)
    client.subscribe(topic)
    client.loop_forever()

# Mosquitto MQTT 브로커 실행
# 여기서는 별도의 스크립트나 터미널에서 Mosquitto를 실행하도록 가정합니다.

main()

# MQTT 클라이언트 설정
client = mqtt.Client("python-mqtt")
broker_instance = mqtt_broker()  # mqtt_broker 클래스 인스턴스 생성

# Publish와 Subscribe를 멀티스레드로 실행
publish_thread = threading.Thread(target=publish_message, args=(client, topic))
subscribe_thread = threading.Thread(target=subscribe_messages, args=(client, topic, broker_instance))

publish_thread.start()
subscribe_thread.start()

# 메인 스레드가 종료되기 전까지 대기
publish_thread.join()
subscribe_thread.join()
