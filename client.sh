#!/bin/sh

PORT=/dev/cu.usbserial-1410

ampy --port $PORT put $PWD/main.py
ampy --port $PORT put $PWD/boot.py
ampy --port $PORT put $PWD/values.py
ampy --port $PORT --baud 115200 run $PWD/client.py