#!/usr/bin/env python3
import serial
import time
import sys
import pycurl
import certifi
import json
import requests
from io import BytesIO

# init data dict
DATA = {
    "hot": 0,
    "warm": 0,
    "cold": 0,
    "snow": 0,
    "rain": 0
}

# initialize serial communication with arduino
#ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#ser.reset_input_buffer()


def get_weather_info():
    """
    CURLs the weather API, stores and returns the desired variables
    as int.
    """

    # API URL
    url = "https://api.open-meteo.com/v1/forecast?latitude=49.14&longitude=9.22&hourly=temperature_2m,rain,snowfall" 
    # Send GET request
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Save data to a JSON file
        filename = "output.json"
        with open(filename, "w") as file:
            json.dump(data, file)


def parse_info():
    """
    Parses JSON file and returns values of temperature, rain and snow
    """

    # load json
    with open("output.json", "r") as f:
        
        data = json.load(f)
        data_dict = dict(data["hourly"])
        # temperature in C
        temp = round(sum(data_dict["temperature_2m"]) / len(data_dict["temperature_2m"]), 2)
        # rain in mm over ground
        rain = round(sum(data_dict["rain"]) / len(data_dict["rain"]), 2)
        # snowfall in cm over ground
        snow = round(sum(data_dict["snowfall"]) / len(data_dict["snowfall"]), 2)

    return temp, rain, snow


def temperature(hot=25, warm=15, cold=5, snow=0.1, rain=0.1):
    """
    Flags temperature with 0 and 1, the options are:
    - Hot
    - Warm
    - Cold
    - Snow
    - Rain
    Modifies global dictionary
    """
    # get info from function
    temp, rain, snow = parse_info()
    # calculate desired temperature:
    # for heat
    if temp >= hot:
        # TODO
        DATA["hot"] = 1
        DATA["warm"] = 0
        DATA["cold"] = 0
        DATA["snow"] = 0
    # for warm
    elif temp < 25 and temp > 10:
        # TODO
        DATA["warm"] = 1
        DATA["hot"] = 0
        DATA["cold"] = 0
        DATA["snow"] = 0
    # for cold 
    elif temp < 10:
        #TODO
        DATA["cold"] = 1
        DATA["warm"] = 0
        DATA["hot"] = 0
    # for snow
    if snow > 0.1:
        #TODO
        DATA["warm"] = 0
        DATA["hot"] = 0
        DATA["snow"] = 1
        DATA["cold"] = 1
        DATA["rain"] = 0
    # for rain
    if rain > 0.1:
        #TODO
        DATA["snow"] = 0
        DATA["rain"] = 1


def send_info():
    """
    Sends the arduino via serial communication a code
    designed to be parsed.
    The code is as follows:
    H()C()W()S()R()
    Where the () will be substitued either by a 0 or 1
    """
    # code the message
    h = DATA["hot"]
    c = DATA["cold"]
    w = DATA["warm"]
    s = DATA["snow"]
    r = DATA["rain"]

    message = f"H{h}C{c}W{w}S{s}R{r}"
    # write to arduino
    ser.write(str(message).encode("ascii"))
    # TODO time.sleep(10) 
    # listen to answer
    ans = ser.readline().decode('utf-8').rstrip()
    # output error
    if ans == 1:
        print("RGB FAILURE")
    elif ans == 2:
        print("STEPPER FAILURE")
    elif ans == 3:
        print("SERVO FAILURE")
    elif ans == 4:
        print("BUZZER FAILURE")


if __name__ == '__main__':

    while True:
        # get api data
        get_weather_info()
        # modify data dictionary 
        temperature()
        # send message
        #send_info()
        # sleep for 1 hour
        time.sleep(3600)