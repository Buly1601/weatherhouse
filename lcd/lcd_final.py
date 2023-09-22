#!/usr/bin/env python3
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # TODO

def send_info():
    """
    Sends info to the arduino that conotrols the LCD
    """
    # get the date and time
    year, month, day, hour, min_ = map(int, time.strftime("%Y %m %d %H %M").split())
    # get temperature
    # TODO
    ans = ""
    hh = "12:25"
    time_ = f"{hour}:{min_}"
    while ans != "12:25":
       ser.write(str(hh).encode("ascii"))
       ans = ser.readline().decode("utf-8").rstrip()
       time.sleep(1)
    print(ans)
    # send date
    date = f"{year}-{month}-{day}"
    ddd = "2001-10-16"
    while ans != ddd:
       ser.write(str(ddd).encode("ascii"))
       ans = ser.readline().decode("utf-8").rstrip()
       time.sleep(1)
    print(ans)
    temp = " 17"
    while ans != "T":
       ser.write(str(temp).encode("ascii"))
       ans = ser.readline().decode("utf-8").rstrip()
       time.sleep(1)
    print(ans)
    time.sleep(10)

if __name__ == "__main__":
    while True:
      send_info()
