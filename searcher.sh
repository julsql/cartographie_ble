#!/bin/sh

PORT=/dev/cu.usbserial-120

echo import searcher > ./main.py
ampy --port $PORT put ./main.py
ampy --port $PORT put ./boot.py
ampy --port $PORT put ./searcher.py
#ampy --port $PORT --baud 115200 run $PWD/searcher.py