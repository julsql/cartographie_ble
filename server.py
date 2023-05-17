import uasyncio as asyncio
import aioble
import bluetooth
import binascii
import struct
import values

# Randomly generated UUIDs.
_SERVICE_UUID = bluetooth.UUID(values.SERVICE_UUID_STR)
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID(values.CHARACTERISTIC_UUID_STR)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Register GATT server.
my_service = aioble.Service(_SERVICE_UUID)
control_characteristic = aioble.Characteristic(
    my_service, _CONTROL_CHARACTERISTIC_UUID, write=True, notify=True
)
aioble.register_services(my_service)

server_mac = ""

async def write(connection, values):
    try:
        print("Sending data")
        my_service = await connection.service(_SERVICE_UUID)
        new_control_characteristic = await my_service.characteristic(
            _CONTROL_CHARACTERISTIC_UUID
        )
        print(values)
        nb_value = len(values)
        await new_control_characteristic.write(struct.pack("<BB", nb_value))
        for value in values:
            await control_characteristic.written()
            msg = control_characteristic.read()
            control_characteristic.write(b"")
            data = msg[0:].decode()
            if data == "value received":
                print("SENDING: ", value)
                await new_control_characteristic.write(value.encode())

    except asyncio.TimeoutError:
        print("Timeout discovering services/characteristics")
        return
    
async def get_neighbour():
    neigh = []
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            if mac != server_mac and mac not in neigh :
                print("MAC ADDRESS: ", mac)
                #print(result, result.name(), result.rssi, result.services())
                neigh.append(mac)
    return neigh

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
            name=values.NAME,
            services=[_SERVICE_UUID],
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

                    data = msg[0:].decode()

                    # Process the received data as needed
                    print("Received data:", data)
                    if data == "look":

                        to_send = await get_neighbour()
                        print("neightbour: ", to_send)

                        await write(connection, to_send)


        except aioble.DeviceDisconnectedError:
            return

# Run both tasks.
async def main():
    await peripheral_task()


asyncio.run(main())