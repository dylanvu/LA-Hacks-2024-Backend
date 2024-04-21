import asyncio
import websockets
from bleak import BleakClient, BleakScanner

haptic_devices = {}
haptic_definition_client_names = {"Haptic Definition: Right Hand", "Haptic Definition: Left Hand", "Haptic Definition: Vest"}

async def main_client(uri):

    print("looking for bluetooth")
    
    # scan for bluetooth devices once
    print("Scanning for bluetooth devices...")
    devices = await BleakScanner.discover()
    for d in devices:
        # print(d)
        if d.name in haptic_definition_client_names:
            async with BleakClient(d) as client:
                client_characteristics = []
                print("Connected to", d.name, "Getting services...")
                client_services_collection = client.services
                client_services = client_services_collection.services
                for service in client_services.values():
                    for characteristic in service.characteristics:
                        if "write" in characteristic.properties:
                            await client.write_gatt_char(characteristic.uuid, "Hello World".encode(), response=False)
                            client_characteristics.append(characteristic)
                haptic_devices.update({d.name: {"client": client, "client_characteristics": client_characteristics}})
    print(haptic_devices)
    if (len(haptic_devices) == 0):
        print("No haptic devices found")
        return
    # now handle the socket events
    print("Ready to connect to websocket server")
    while(True):
        # try:
            
        connection_state = {"is_open": True}
        websocket = await websockets.connect(uri)
        try:
            async for message in websocket:
                print("Received message:", message)
                # broadcast the message to all haptic devices
                for device_name in haptic_devices:
                    print(device_name)
                    device = haptic_devices[device_name]["client"]
                    characteristics = haptic_devices[device_name]["client_characteristics"]
                    for characteristic in characteristics:
                        # TODO: I get an error if I try to write to the characteristic here
                        # await device.write_gatt_char(characteristic.uuid, message.encode(), response=False)
                        pass


        except websockets.exceptions.ConnectionClosed:
            print("Connection closed by server.")
        # except Exception as e:
        #     print(f"WebSocket Error: {e}")
        finally:
            connection_state["is_open"] = False

        # except Exception as e:
        #     print(e)
        #     pass
        

uri = "ws://localhost:5000"
asyncio.run(main_client(uri))