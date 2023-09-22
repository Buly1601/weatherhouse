#!/usr/bin/env python3
from datetime import datetime
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # TODO

def send_info():
    """
    Sends info to the arduino that conotrols the LCD
    """
    # get the date and time
    now = datetime.now()
    datetime_str = now.strftime("%H:%M%Y-%m-%d")
    #year, month, day, hour, min_ = map(int, time.strftime("%Y %m %d %H %M").split()) # TODO
    # get temperature
    # TODO
    
    ans = ""
    temp = "+23"
    datetime_str += temp
    memo = ""
    #data = f"{hour}:{min_}{year}-{month}-{day}{temp}"
    #print(data)
    for i,j in enumerate(datetime_str):
        if j == "0":
            memo += "O"
        else:
            memo += j
    #data_ = "12:252OO1-1O-16+17"

    while ans != "1":
        ser.write(str(memo).encode("ascii"))
        time.sleep(2)
        ans = ser.readline().decode("utf-8").rstrip()
        print(ans)

if __name__ == "__main__":
    while True:
      send_info()
      time.sleep(10)
