import uasyncio as asyncio
import aioble
import bluetooth
import binascii
import values
import struct 
import ubinascii
import machine
import neopixel

num_leds = 1

led_pin = machine.Pin(48, machine.Pin.OUT)
leds = neopixel.NeoPixel(led_pin, num_leds)

def led_on(color="green"):
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

# Register GATT server.
my_service = aioble.Service(_SERVICE_UUID)
control_characteristic = aioble.Characteristic(
    my_service, _CONTROL_CHARACTERISTIC_UUID, write=True, notify=True
)
aioble.register_services(my_service)

class Client:
    def __init__(self, device):
        self._device = device
        self._connection = None
        self._seq = 1

    async def connect(self):
        try:
            self._connection = await self._device.connect()
        except asyncio.TimeoutError:
            print("Timeout during connection")
            return

        try:
            my_service = await self._connection.service(_SERVICE_UUID)
            self._control_characteristic = await my_service.characteristic(
                _CONTROL_CHARACTERISTIC_UUID
            )
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

    async def send_message(self, message):
        await self._command(message.encode())

    async def ask_neighboor(self, macs):
        # On envoie les macs des ESP qu'on a déjà consulté
        await self.send_list(macs)
        #await self.send_message("ok to receive")
        await control_characteristic.written()
        msg = control_characteristic.read()
        control_characteristic.write(b"")
        data = msg[0:].decode()
        if data == "value received":
            await self._control_characteristic.write("ok to receive".encode())
        response = await self.get_response()
        return response


    async def send_list(self, values):
        try:
            nb_value = len(values)
            await self._control_characteristic.write(struct.pack("<BB", nb_value))
            for value in values:
                await control_characteristic.written()
                msg = control_characteristic.read()
                control_characteristic.write(b"")
                data = msg[0:].decode()
                if data == "value received":
                    await self._control_characteristic.write(value.encode())

        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

    async def get_response(self):
        await control_characteristic.written()
        msg = control_characteristic.read()
        control_characteristic.write(b"")
        nb_values = int(msg[0])
        data_complete = []
        for _ in range(0, nb_values):
            await self.send_message("value received")
            await control_characteristic.written()
            msg = control_characteristic.read()
            control_characteristic.write(b"")
            data = msg[0:].decode()
            data_complete.append(data)

        return data_complete

    async def _command(self, data):
        send_seq = self._seq
        await self._control_characteristic.write(data)
        self._seq += 1
        return send_seq

    async def disconnect(self):
        if self._connection:
            await self._connection.disconnect()

def get_mac_address(mac_bytes):
    # result.device.addr
    mac_string = binascii.hexlify(mac_bytes).decode('utf-8')
    formatted_mac = ':'.join(mac_string[i:i+2].upper() for i in range(0, 12, 2))
    return formatted_mac

async def main():
    devices = []
    tree = {}
    macs = []
    async with aioble.scan(5000, 60000, 60000, active=True) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            tree[mac] = []
            if result.name() == values.NAME and _SERVICE_UUID in result.services():
                if mac not in macs:
                    macs.append(mac)
                    devices.append(result.device)
                
        else:
            if (len(devices) == 0):
                print("No other ESP found")
                return tree

    for device in devices:
        client = Client(device)

        await client.connect()
        
        response = await client.ask_neighboor(macs)
        liste = []
        for mac_response in response:
            liste.append({mac_response : []})
        tree[get_mac_address(device.addr)] = liste
        await client.disconnect()

    return tree

led_on("green")
print("READY TO SEARCH")
tree = asyncio.run(main())
led_off()

# Récupérer l'adresse MAC de l'ESP32
def get_mac():
    return(ubinascii.hexlify(machine.unique_id(), ':').decode().upper())

def print_tree(tree, level=0, printed_devices=[]):
    if len(printed_devices) == 0:
        print(f'| {get_mac()}')
        level += 1
    for key, value in tree.items():
        if key not in printed_devices:
            indent = ' ' * 20 * level
            print(f'{indent}| {key}')
            printed_devices.append(key)
            if value != []:
                for dico in value:
                    print_tree(dico, level+1, printed_devices)

print_tree(tree)
