#!/bin/sh

PORT=/dev/cu.usbserial-110

echo import receiver > ./main.py
ampy --port $PORT put ./main.py
ampy --port $PORT put ./receiver.py
#ampy --port $PORT --baud 115200 run $PWD/receiver.py