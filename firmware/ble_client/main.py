import asyncio
import websockets
import json
from bleak import BleakClient, BleakScanner

haptic_devices = []

async def main_client(uri):

    print("looking for bluetooth")
    
    # scan for bluetooth devices once
    print("Scanning for bluetooth devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        # print(d)
        if d.name == "Haptic Definition: Right Hand":
            async with BleakClient(d) as client:
                haptic_devices.append(client)
                print(d.name)
                # while connection_state["is_open"]:
                #     asyncio.sleep(1)
    print(haptic_devices)
    # now handle the socket events
    while(True):
        try:
            
            connection_state = {"is_open": True}
            websocket = await websockets.connect(uri)
            try:
                async for message in websocket:
                    print("Received message:", message)
                    # data = json.loads(message)
                    # print("Received message:", data)

            except websockets.exceptions.ConnectionClosed:
                print("Connection closed by server.")
            except Exception as e:
                print(f"WebSocket Error: {e}")
            finally:
                connection_state["is_open"] = False

        except Exception as e:
            pass
        

uri = "ws://localhost:5000"
asyncio.run(main_client(uri))