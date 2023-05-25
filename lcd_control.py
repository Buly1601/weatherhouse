#!/usr/bin/env python3
import time
import serial

ser = ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # TODO

def send_info():
    """
    Sends info to the arduino that conotrols the LCD
    """
    # get the date and time
    year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
    # get temperature
    # TODO
    # send date
    date = f"{year}-{month}-{day}"
    ser.write(str(date).encode("ascii"))
    time.sleep(1)
    # send time
    time = f"{hour}:{min}"
    ser.write(str(time).encode("ascii"))
    temp = " 17"
    ser.write(str(temp).encode("ascii"))
if __name__ == "__main__":
    send_info()