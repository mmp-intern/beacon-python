import paho.mqtt.client as mqtt
import numpy as np
import json
from collections import defaultdict

# MQTT 브로커 정보 설정
broker_address = "192.168.0.71"  # 브로커의 주소
broker_port = 1883  # 브로커의 포트

# 클라이언트 생성
client = mqtt.Client()

# MAC 주소별로 데이터를 저장하기 위한 딕셔너리
mac_data = defaultdict(list)

class KalmanFilter:
    def __init__(self, initial_state, initial_covariance, measurement_noise, process_noise):
        self.state = initial_state
        self.covariance = initial_covariance
        self.measurement_noise = measurement_noise
        self.process_noise = process_noise

    def predict(self):
        # Prediction step
        # Example: Assuming no change in state for simplicity
        return self.state

    def update(self, measurement):
        # Update step
        # Example: Simple update with measurement
        K = self.covariance / (self.covariance + self.measurement_noise)
        self.state = self.state + K * (measurement - self.state)
        self.covariance = (1 - K) * self.covariance

    def get_state(self):
        return self.state

# 예시 사용
initial_state = np.array([0.0])  # 초기 상태 벡터
initial_covariance = np.array([1.0])  # 초기 공분산 행렬
measurement_noise = 1.0  # 측정 잡음
process_noise = 0.1  # 프로세스 잡음

kalman_filter = KalmanFilter(initial_state, initial_covariance, measurement_noise, process_noise)


# 연결 이벤트 핸들러
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # 연결되면 구독 신청
    client.subscribe("/gw/ac233fc18bf0/status")  # 구독할 토픽명 입력
    
def process_rssi_data(mac_data):
    for mac, data in mac_data.items():
        for entry in data:
            rssi_measurement = entry['rssi']
            kalman_filter.update(rssi_measurement)
            filtered_rssi = kalman_filter.get_state()
            # 여기에 위치 추정 로직을 추가하여 필요한 처리를 수행한다.

# 메시지 수신 이벤트 핸들러
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode('utf-8'))
    for item in data:
        if "timestamp" in item and "mac" in item and "rssi" in item and 'ibeaconTxPower' in item:
            mac_data[item["mac"]].append({
                "timestamp": item["timestamp"],
                "mac": item["mac"],
                "rssi": item["rssi"],
                "ibeaconTxPower": item["ibeaconTxPower"]
            })

    process_rssi_data(mac_data)

    # 필터링된 결과를 저장하거나 추가적인 처리를 수행할 수 있음

    with open('test_data5.json', 'w') as json_file:
        json.dump(mac_data, json_file, indent=4)

    print("Filtered data saved to 'filtered_data.json'")

# 연결 이벤트 핸들러 등록
client.on_connect = on_connect

# 메시지 수신 이벤트 핸들러 등록
client.on_message = on_message

# 브로커에 연결
client.connect(broker_address, broker_port, 60)

# 통신 시작 (블로킹 함수)
client.loop_forever()
