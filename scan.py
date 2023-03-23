# Fichier scan.py --> Scanner les périphériques BLE détéctables par la ESP32-S3

import uasyncio as asyncio
import aioble

print("Scan des périphériques BLE détéctables")

async def main():
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())
            

asyncio.run(main())