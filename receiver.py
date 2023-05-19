import uasyncio as asyncio
import aioble
import bluetooth
import binascii
import struct
import values

import machine
import neopixel

num_leds = 1

led_pin = machine.Pin(48, machine.Pin.OUT)
leds = neopixel.NeoPixel(led_pin, num_leds)

def led_on(color="blue"):
    if color == "red":
        leds[0] = (255, 0, 0)
    if color == "green":
        leds[0] = (0, 255, 0)
    if color == "blue":
        leds[0] = (0, 0, 255)
    leds.write()
    
def led_off():

    leds[0] = (0, 0, 0)
    leds.write()


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

async def send_message(connection, message):
    try:
        my_service = await connection.service(_SERVICE_UUID)
        new_control_characteristic = await my_service.characteristic(
            _CONTROL_CHARACTERISTIC_UUID
        )
        await new_control_characteristic.write(message.encode())

    except asyncio.TimeoutError:
        print("Timeout discovering services/characteristics")
        return

async def send_list(connection, values):
    try:
        my_service = await connection.service(_SERVICE_UUID)
        new_control_characteristic = await my_service.characteristic(
            _CONTROL_CHARACTERISTIC_UUID
        )
        nb_value = len(values)
        await new_control_characteristic.write(struct.pack("<BB", nb_value))
        for value in values:
            await control_characteristic.written()
            msg = control_characteristic.read()
            control_characteristic.write(b"")
            data = msg[0:].decode()
            if data == "value received":
                await new_control_characteristic.write(value.encode())

    except asyncio.TimeoutError:
        print("Timeout discovering services/characteristics")
        return
    
async def get_neighbour(forbidden):
    neigh = []
    async with aioble.scan(5000, 60000, 60000, active=True) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            if mac != server_mac and mac not in neigh and not mac in forbidden :
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
        connection = await aioble.advertise(
            _ADV_INTERVAL_MS,
            name=values.NAME,
            services=[_SERVICE_UUID],
        )
        global server_mac
        server_mac = get_mac_address(connection.device.addr)


        try:
            with connection.timeout(None):
                while True:
                    await control_characteristic.written()
                    msg = control_characteristic.read()
                    control_characteristic.write(b"")

                    data = msg[0]

                    # Process the received data as needed
                    
                    try:
                        nb_values = int(data)
                    except:
                        print ('wrong value send')
                    else:
                        already_ESP = []
                        await send_message(connection, "value received")
                        for _ in range(0, nb_values):
                            await control_characteristic.written()
                            msg = control_characteristic.read()
                            control_characteristic.write(b"")
                            data = msg[0:].decode()
                            
                            already_ESP.append(data)
                            await send_message(connection, "value received")

                        await control_characteristic.written()
                        msg = control_characteristic.read()
                        control_characteristic.write(b"")
                        data = msg[0:].decode()
                        if data == "ok to receive":
                            to_send = await get_neighbour(already_ESP)

                            await send_list(connection, to_send)
                        else:
                            print("error")

        except aioble.DeviceDisconnectedError:
            led_off()
            return

# Run both tasks.
async def main():
    led_on("blue")
    await peripheral_task()
    led_off()

print("READY TO RECEIVE")
asyncio.run(main())