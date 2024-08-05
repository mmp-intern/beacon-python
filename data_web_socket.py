import asyncio
import websockets
import json


async def send_beacon_data(file_path):
    uri = "ws://localhost:8080/ws/beacon"
    async with websockets.connect(uri) as websocket:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # 변환된 형식의 데이터 생성
        beacon_data = {
            "gateways": []
        }

        for gatewayMac, beacons in data.items():
            gateway_entry = {
                "gatewayMac": gatewayMac,
                "beacons": []
            }
            for mac, info in beacons.items():
                beacon_entry = {
                    "mac": mac,
                    "earlyTimestamp": info["early_timestamp"],
                    "lateTimestamp": info["late_timestamp"]
                }
                gateway_entry["beacons"].append(beacon_entry)
            beacon_data["gateways"].append(gateway_entry)

        await websocket.send(json.dumps(beacon_data))
        print(f"Send: {json.dumps(beacon_data, indent=2)}")

        try:
            response = await websocket.recv()
            print(f"Received: {response}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(send_beacon_data())