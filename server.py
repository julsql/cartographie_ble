import uasyncio as asyncio
import aioble
import bluetooth


# Randomly generated UUIDs.
_FILE_SERVICE_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130002")
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130003")

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Register GATT server.
file_service = aioble.Service(_FILE_SERVICE_UUID)
control_characteristic = aioble.Characteristic(
    file_service, _CONTROL_CHARACTERISTIC_UUID, write=True, notify=True
)
aioble.register_services(file_service)

async def control_task(connection):
    try:
        with connection.timeout(None):
            while True:
                print("Waiting for write")
                await control_characteristic.written()
                msg = control_characteristic.read()
                control_characteristic.write(b"")

                if len(msg) < 3:
                    continue

                # Message is <command><seq><path...>.

                command = msg[0]
                seq = msg[1]
                data = msg[2:].decode()

                return data
            
    except aioble.DeviceDisconnectedError:
        return
    

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        print("")
        print("Waiting for connection")
        connection = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="mpy-file",
            services=[_FILE_SERVICE_UUID],
        )
        print("Connection from", connection.device)

        try:
            with connection.timeout(None):
                while True:
                    print("Waiting for write")
                    await control_characteristic.written()
                    msg = control_characteristic.read()
                    control_characteristic.write(b"")

                    if len(msg) < 3:
                        continue

                    # Message is <command><seq><path...>.
                    command = msg[0]
                    seq = msg[1]
                    data = msg[2:]

                    # Process the received data as needed
                    print("Received data:", data.decode())

        except aioble.DeviceDisconnectedError:
            return

# Run both tasks.
async def main():
    await peripheral_task()


asyncio.run(main())