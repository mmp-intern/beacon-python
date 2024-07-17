import paho.mqtt.client as mqtt

# 브로커 설정
broker_host = "192.168.0.71"  # MQTT 브로커 호스트
broker_port = 1883  # MQTT 브로커 포트

# 서브스크라이버들이 구독할 토픽들
topics = ["/gw/scanpub/40d63cd705ba", "/gw/scanpub/40d63cd6fd92"]

# 각 토픽에 대한 메시지가 도착했을 때의 콜백 함수
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' from topic '{message.topic}'.")

# MQTT 클라이언트 생성 및 설정
clients = []
for topic in topics:
    client = mqtt.Client()
    client.on_message = on_message
    clients.append(client)

# 각 클라이언트에 토픽들에 대해 구독 설정
for idx, client in enumerate(clients):
    client.connect(broker_host, broker_port, 60)
    print(f"Client {idx+1} connected to broker '{broker_host}:{broker_port}'. Subscribing to topic '{topics[idx]}'...")
    client.subscribe(topics[idx])

# 메시지를 처리할 때까지 유지
for client in clients:
    client.loop_forever()
