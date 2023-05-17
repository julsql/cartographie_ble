#!/bin/sh

ampy --port /dev/cu.usbserial-110 --baud 115200 run $PWD/server.py