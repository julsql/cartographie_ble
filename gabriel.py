import uasyncio as asyncio
import aioble

print("Scan des périphériques BLE détéctables")

device def main():
#    async with aioble.scan(duration_ms=5000, interval_us=30000, window_us=30000, active=True) as scanner:
#        async for result in scanner:
#            print(result, result.name(), result.rssi, result.services())           

# Either from scan result
    device = result.device
# Or with known address
    device = aioble.Device(aioble.PUBLIC, "aa:bb:cc:dd:ee:ff")

    try:
        connection = await device.connect(timeout_ms=2000)
    except asyncio.TimeoutError:
        print('Timeout')

asyncio.run(main())