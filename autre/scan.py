# Fichier scan.py --> Scanner les périphériques BLE détéctables par la ESP32-S3

import uasyncio as asyncio
import aioble
import binascii

print("Scan des périphériques BLE détéctables")

theo = "7C:DF:A1:E7:D0:66"

def get_mac_address(mac_bytes):
    # result.device.addr
    mac_string = binascii.hexlify(mac_bytes).decode('utf-8')
    formatted_mac = ':'.join(mac_string[i:i+2].upper() for i in range(0, 12, 2))
    return formatted_mac

async def main():
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            print("MAC ADDRESS: ", mac)
            if mac == theo:
                print(result, result.name(), result.rssi, result.services())
            

asyncio.run(main())
