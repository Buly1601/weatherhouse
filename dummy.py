#!/usr/bin/env python3
import serial
import time
import sys
import pycurl
import certifi
import json
import requests
from io import BytesIO

# init data dict temp, rain, snow, prec, cloud, wind, visi
DATA = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "U": 0,
    "N": 0,
    "W": 0,
    "R": 0
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
    url = "https://api.open-meteo.com/v1/forecast?latitude=49.14&longitude=9.22&hourly=temperature_2m,precipitation,rain,snowfall,cloudcover,visibility,windgusts_10m" 
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
        try:
            temp = round(sum(data_dict["temperature_2m"]) / len(data_dict["temperature_2m"]), 2)
        except:
            temp = 0
        # rain in mm over ground
        try:
            rain = round(sum(data_dict["rain"]) / len(data_dict["rain"]), 2)
        except:
            rain = 0
        # snowfall in cm over ground
        try: 
            snow = round(sum(data_dict["snowfall"]) / len(data_dict["snowfall"]), 2)
        except:
            snow = 0
        # ! FLAGS
        # precipitation in mm
        try:
            prec =  round(sum(data_dict["precipitation"]) / len(data_dict["precipitation"]), 2)
        except:
            prec = 0
        # cloudcover total in %
        cloud = data_dict["cloudcover"]
        # wind gusts in km/h
        try:
            wind = round(sum(data_dict["windgusts_10"]) / len(data_dict["windgusts_10"]), 2)
        except:
            wind = 0
        # visibility in meters (max is 24)
        visi = data_dict["visibility"]

    return temp, rain, snow, prec, cloud, wind, visi


def temperature(h=25, c=5, sn=0.1, r=0.1, pr=0.05, cl=40, w=10, v=15):
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
    temp, rain, snow, prec, cloud, wind, visi = parse_info()
    # calculate desired temperature:
    # for snow
    if snow > sn:
        #TODO
        DATA["1"] = 0
        DATA["3"] = 1
        DATA["2"] = 0
        DATA["4"] = 0
    # for rain
    elif rain > r:
        #TODO
        DATA["1"] = 0
        DATA["3"] = 0
        DATA["2"] = 0
        DATA["4"] = 1
    # for heat
    elif temp >= h:
        # TODO
        DATA["1"] = 1
        DATA["3"] = 0
        DATA["2"] = 0
        DATA["4"] = 0
    # for cold 
    elif temp < c:
        #TODO
        DATA["1"] = 0
        DATA["3"] = 0
        DATA["2"] = 1
        DATA["4"] = 0
    # ! FLAGS
    if prec > pr:
        DATA["R"] = 1
    else:
        DATA["R"] = 0
    if cloud > cl:
        DATA["N"] = 1
    else:
        DATA["N"] = 0
    if wind > w:
        DATA["W"] = 1
    else:
        DATA["W"] = 0
    if visi > v:
        DATA["U"] = 1
    else:
        DATA["U"] = 0


def send_info():
    """
    Sends the arduino via serial communication a code
    designed to be parsed.
    The code is as follows:
    NUMBER LETTER LETTER LETTER LETTER
    Where LETTER will be substitued either by a 0 or a letter if 
    the case.
    """
    # init message
    message = ""
    # code the message
    for key,value in DATA.items():
        if value == 1:
            message += key

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