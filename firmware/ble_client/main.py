import asyncio
import websockets
import json
from bleak import BleakClient, BleakScanner

def trigger_haptics():
    print("haptics triggered")

async def connect_to_bluetooth(websocket, connection_state):
    print("looking for bluetooth")
    
    # scan for bluetooth devices once


    print("Scanning for bluetooth devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        if d.name == "Haptic Definition: Right Hand":
            async with BleakClient(d) as client:
                print(d.name)
                while connection_state["is_open"]:
                    asyncio.sleep(1)

async def receive_events(websocket, connection_state):
    try:
        async for message in websocket:
            print("Received message:", message)
            # data = json.loads(message)
            # print("Received message:", data)

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by server.")
    finally:
        connection_state["is_open"] = False

async def main_client(uri):
    while(True):
        try:
            
            connection_state = {"is_open": True}

            try:
                async with websockets.connect(uri) as websocket:
                    # Create a task for send_frames
                    connect_bluetooth_task = asyncio.create_task(connect_to_bluetooth(websocket, connection_state))
                    # Create a task for receive_events
                    receive_events_task = asyncio.create_task(receive_events(websocket, connection_state))
                    
                    # Wait for tasks to complete
                    await asyncio.gather(connect_bluetooth_task, receive_events_task)
                        

            except Exception as e:
                print(f"WebSocket Error: {e}")
        except Exception as e:
            pass
        

uri = "ws://localhost:5000"
asyncio.run(main_client(uri))