# MIT license; Copyright (c) 2021 Jim Mussared

# This is a WIP client for l2cap_file_server.py. See that file for more
# information.

import sys

sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

import struct

_FILE_SERVICE_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130002")
_CONTROL_CHARACTERISTIC_UUID = bluetooth.UUID("0492fcec-7194-11eb-9439-0242ac130003")

_COMMAND_SEND = const(0)

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

class Client:
    def __init__(self, device):
        self._device = device
        self._connection = None
        self._seq = 1

    async def connect(self):
        try:
            print("Connecting to", self._device)
            self._connection = await self._device.connect()
            print(type(self._connection))
        except asyncio.TimeoutError:
            print("Timeout during connection")
            return

        try:
            print("Discovering...")
            file_service = await self._connection.service(_FILE_SERVICE_UUID)
            self._control_characteristic = await file_service.characteristic(
                _CONTROL_CHARACTERISTIC_UUID
            )
        except asyncio.TimeoutError:
            print("Timeout discovering services/characteristics")
            return

    async def send_message(self, message):
        print("Sending message:", message)
        await self._command(_COMMAND_SEND, message.encode())

    async def get_response(self):
        await control_characteristic.written()
        msg = control_characteristic.read()
        control_characteristic.write(b"")

        return msg[0:].decode()

    async def _command(self, cmd, data):
        send_seq = self._seq
        await self._control_characteristic.write(struct.pack("<BB", cmd, send_seq) + data)
        self._seq += 1
        return send_seq

    async def disconnect(self):
        if self._connection:
            await self._connection.disconnect()

import binascii

def get_mac_address(mac_bytes):
    # result.device.addr
    mac_string = binascii.hexlify(mac_bytes).decode('utf-8')
    formatted_mac = ':'.join(mac_string[i:i+2].upper() for i in range(0, 12, 2))
    return formatted_mac

devices = []
tree = {}

async def main():
    async with aioble.scan(5000, 30000, 30000, active=True) as scanner:
        async for result in scanner:
            mac = get_mac_address(result.device.addr)
            tree[mac] = []
            if result.name() == "esp-server" and _FILE_SERVICE_UUID in result.services():
                print(mac)
                #if mac == "7C:DF:A1:E7:D0:66":
                devices.append(result.device)
                
        else:
            if (len(devices) == 0):
                print("File server not found")
                return

    for device in devices:
        client = Client(device)

        await client.connect()
        
        await client.send_message("look")

        response = await client.get_response()
        print("Received data:", response)
        tree[get_mac_address(device.addr)] = response.split(",")

        await client.disconnect()
    print("tree", tree)

asyncio.run(main())
