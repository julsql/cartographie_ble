import uasyncio as asyncio
import aioble
import bluetooth
import struct
from micropython import const

# Randomly generated UUIDs.
_FILE_SERVICE_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130002")
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130003")
_COMMAND_SEND = const(0)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Register GATT server.
file_service = aioble.Service(_FILE_SERVICE_UUID)
control_characteristic = aioble.Characteristic(
    file_service, _CONTROL_CHARACTERISTIC_UUID, write=True, notify=True
)
aioble.register_services(file_service)

server_mac = ""

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
    
async def write(connection, data):
    try:
        print("Sending data")
        file_service = await connection.service(_FILE_SERVICE_UUID)
        new_control_characteristic = await file_service.characteristic(
            _CONTROL_CHARACTERISTIC_UUID
        )
        await new_control_characteristic.write(struct.pack("<BB", _COMMAND_SEND, 1) + data.encode())


    except asyncio.TimeoutError:
        print("Timeout discovering services/characteristics")
        return
    
async def get_neighbour():
    neigh = ""
    async with aioble.scan(duration_ms=5000) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            print("MAC ADDRESS: ", mac)
            if mac != server_mac:
                print(result, result.name(), result.rssi, result.services())
                neigh += mac + ","
    return neigh[:-1]
    
import binascii

def get_mac_address(mac_bytes):
    # result.device.addr
    mac_string = binascii.hexlify(mac_bytes).decode('utf-8')
    formatted_mac = ':'.join(mac_string[i:i+2].upper() for i in range(0, 12, 2))
    return formatted_mac

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        print("")
        print("Waiting for connection")
        connection = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="esp-server",
            services=[_FILE_SERVICE_UUID],
        )
        print("Connection from", connection.device)
        global server_mac
        server_mac = get_mac_address(connection.device.addr)


        try:
            with connection.timeout(None):
                while True:
                    print("Waiting for write")
                    await control_characteristic.written()
                    msg = control_characteristic.read()
                    control_characteristic.write(b"")

                    print(dir(control_characteristic))

                    if len(msg) < 3:
                        continue

                    # Message is <command><seq><path...>.
                    command = msg[0]
                    seq = msg[1]
                    data = msg[2:].decode()

                    # Process the received data as needed
                    print("Received data:", data)
                    if data == "look":

                        to_send = get_neighbour()

                        await write(connection, to_send)


        except aioble.DeviceDisconnectedError:
            return

# Run both tasks.
async def main():
    await peripheral_task()


asyncio.run(main())