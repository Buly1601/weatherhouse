#!/bin/bash

arduino-cli compile --fqbn arduino:avr:mega arduino_scripts.ino

arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega arduino_scripts.ino
