import uasyncio as asyncio
import aioble

print("Scan des périphériques BLE détéctables")

async def main():
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            print(result, result.name(), result.rssi, result.services())
            print("result", result)
            print("result.name()", result.name())
            print("result.rssi", result.rssi)
            print("result.services()", result.services())

asyncio.run(main())