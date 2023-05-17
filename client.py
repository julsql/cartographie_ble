import uasyncio as asyncio
import aioble
import bluetooth
import binascii
import values

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
            print("Connecting to", self._device)
            self._connection = await self._device.connect()
        except asyncio.TimeoutError:
            print("Timeout during connection")
            return

        try:
            print("Discovering...")
            my_service = await self._connection.service(_SERVICE_UUID)
            self._control_characteristic = await my_service.characteristic(
                _CONTROL_CHARACTERISTIC_UUID
            )
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

    async def send_message(self, message):
        print("Sending message:", message)
        await self._command(message.encode())

    async def get_response(self):
        await control_characteristic.written()
        msg = control_characteristic.read()
        control_characteristic.write(b"")
        nb_value = int(msg[0])
        data_complete = []
        for i in range(0, nb_value):
            print("VALUE {}/{} RECEIVED".format(i+1, nb_value))
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
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            tree[mac] = []
            if result.name() == values.NAME and _SERVICE_UUID in result.services():
                if mac not in macs:
                    print(mac)
                    macs.append(mac)
                    devices.append(result.device)
                #break
                
        else:
            if (len(devices) == 0):
                print("No other ESP found")
                return tree
            
    print(devices)
    for device in devices:
        client = Client(device)

        await client.connect()
        
        await client.send_message("look")

        response = await client.get_response()
        print("Received data:", response)
        tree[get_mac_address(device.addr)] = response

        await client.disconnect()

    return tree

tree = asyncio.run(main())
print("tree: ", tree)
