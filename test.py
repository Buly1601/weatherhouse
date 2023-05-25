#!/usr/bin/env python3
import serial
import time
import sys
import pycurl
import certifi
import json
import requests
from io import BytesIO


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# init message
message = "1WUR0"
message_2 = "3"
# code the message
ans = ""
# write to arduino
while True: 
    # listen to answer
    if ans != "2":
      ans = ser.readline().decode('utf-8').rstrip()
      ser.write(message.encode("ascii"))
      print(ans)
    time.sleep(1)
    if ans == "2":
        time.sleep(20)
        ans = ""
