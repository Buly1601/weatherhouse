#!/usr/bin/env python3
import board
import busio
import os
import displayio
from lcd.gauge import Gauge  # Make sure to download the Gauge library from: https://github.com/benevpi/Circuit-Python-Gauge
import adafruit_ili9341

displayio.release_displays()

board_type = os.uname().machine
print(f"Board: {board_type}")

# Define the appropriate pins for the Raspberry Pi 3B
mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.D10, board.D11, board.D17, board.D18, board.D27


spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = adafruit_ili9341.ILI9341(display_bus, width=240, height=320, rotation=270)

gauge = Gauge(0, 100, 120, 120, value_label="x:", arc_colour=0xFF0000, colour=0xFFFF00, outline_colour=0xFFFF00)
gauge.x = 60
gauge.y = 0

gauge2 = Gauge(0, 100, 120, 120, value_label="y:", arc_colour=0xFF0000, colour=0xFFFF00, outline_colour=0xFFFF00)
gauge2.x = 60
gauge2.y = 150

group = displayio.Group(scale=1)

group.append(gauge)
group.append(gauge2)

display.show(group)
display.auto_refresh = True

x = 0
y = 100

while True:
    while x < 100:
        x += 2
        y -= 2
        gauge.update(x)
        gauge2.update(y)

    while x > 0:
        x -= 2
        y += 2
        gauge.update(x)
        gauge2.update(y)

    while x < 100:
        x += 5
        y -= 5
        gauge.update(x)
        gauge2.update(y)

    while x > 0:
        x -= 5
        y += 5
        gauge.update(x)
        gauge2.update(y)
