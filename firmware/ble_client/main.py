import asyncio
from bleak import BleakClient, BleakScanner

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        if (d.name == "Haptic Definition: Right Hand"):
            async with BleakClient(d) as client:
                print("Connected to", d.name)
                print(client.services)
    # hang
    await asyncio.sleep(100.0)

asyncio.run(main())