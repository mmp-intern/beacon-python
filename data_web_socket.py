import asyncio
import websockets
import json


async def send_beacon_data():
    uri = "ws://localhost:8080/ws/beacon"
    async with websockets.connect(uri) as websocket:
        beacon_data = {
            "gateways": [
                {
                    "gatewayMac": "40D63CD6FD92",
                    "beacons": [
                        {
                            "mac": "F4741C781187",
                            "earlyTimestamp": "2024-07-23T16:00:00.000000+00:00",
                            "lateTimestamp": "2024-07-23T16:00:00.000000+00:00"
                        },
                        {
                            "mac": "DE42759B6E12",
                            "earlyTimestamp": "2024-07-23T16:00:00.000000+00:00",
                            "lateTimestamp": "2024-07-23T16:00:00.000000+00:00"
                        }
                    ]
                },
                {
                    "gatewayMac": "50D63CD6FD93",
                    "beacons": [
                        {
                            "mac": "A1741C781187",
                            "earlyTimestamp": "2024-07-23T16:00:00.000000+00:00",
                            "lateTimestamp": "2024-07-23T16:00:00.000000+00:00"
                        },
                        {
                            "mac": "BE42759B6E12",
                            "earlyTimestamp": "2024-07-23T16:00:00.000000+00:00",
                            "lateTimestamp": "2024-07-23T16:00:00.000000+00:00"
                        }
                    ]
                }
            ]
        }

        await websocket.send(json.dumps(beacon_data))
        print(f"Send: {json.dumps(beacon_data, indent=2)}")

        try:
            response = await websocket.recv()
            print(f"Received: {response}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(send_beacon_data())