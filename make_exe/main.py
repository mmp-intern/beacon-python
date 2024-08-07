import asyncio
import time
from mqtt import mqtt_sub, mqtt_broker
from send_data import HandlingJsonFile

async def main():
    broker_address = "192.168.0.71"
    broker_port = 1883

    # Initialize MQTT broker and client
    broker = mqtt_broker()
    broker.broker_start()

    sub = mqtt_sub(broker_address, broker_port)
    sub.start()

    # Initialize HandlingJsonFile
    handler = HandlingJsonFile()

    # Start send_beacon_data in the background
    send_data_task = asyncio.create_task(handler.send_beacon_data())

    try:
        # Keep the main event loop running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Stop MQTT client loop and terminate broker
        sub.client.loop_stop()
        broker.terminate()

        # Ensure send_beacon_data is properly stopped (optional)
        send_data_task.cancel()
        try:
            await send_data_task
        except asyncio.CancelledError:
            print("send_beacon_data task cancelled.")

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())