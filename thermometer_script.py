#!/usr/bin/env python3

""" Short and quick script for reading temp and humidity sensor,
save data to RRD and display the values on the segmented display.
Wetzl Viktor - 2023.03.25
"""

# pylint: disable = import-error
import os
import time
import rrdtool
import board
from adafruit_ht16k33 import segments
import AM2315


def sensor_graph(filepath, rrd_type):
    """ Generate graph from rrd database, according to it's type. """
    loc_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    graph_filename = f"{filepath}.png"
    rrd_filename = f"{filepath}.rrd"

    if rrd_type == "temp":
        rrdtool.graph(graph_filename,
        "-v", "Hőmérséklet [°C]",
        "-t", "Idő [s]",
        "-e", "now",
        "-s", "e-24h",
        #"-S", "300",
        "-w", "1600",
        "-h", "800",
        "-u", "40",
        "-l", "10",
        "--allow-shrink",
        #"-g", # No legend
        "-n", "DEFAULT:10:Arial", # Font
        "-W", "Wetzl Viktor @ " + loc_time,
        f"DEF:ds01={rrd_filename}:temp:AVERAGE",
        "AREA:ds01#3399FF", #60% kék
        "LINE2:ds01#004D99") # 40% kék

    elif rrd_type == "humi":
        rrdtool.graph(graph_filename,
        "-v", "Páratartalom [%]",
        "-t", "Idő [s]",
        "-e", "now",
        "-s", "e-24h",
        #"-S", "300",
        "-w", "1600",
        "-h", "800",
        "-u", "60",
        "-l", "20",
        "--allow-shrink",
        #"-g", # No legend
        "-n", "DEFAULT:10:Arial", # Font
        "-W", "Wetzl Viktor @ " + loc_time,
        f"DEF:ds01={rrd_filename}:humi:AVERAGE",
        "AREA:ds01#75FF33", #60% zöld
        "LINE2:ds01#41CC00") # 40% zöld


def read_data():
    """ Read data from AM2315 sensor using i2C.
    """
    thsen = AM2315.AM2315(powerpin=6)
    humi, temp = thsen.read_humidity_temperature()
    temperature = f"{temp:3.1f}"
    humidity = f"{humi:3.1f}"

    # Update RRD and generate charts
    os.path.join(INITDIR, "temp1.rrd")
    rrdtool.update(os.path.join(INITDIR, "temp1.rrd"), f"N:{temperature}")
    rrdtool.update(os.path.join(INITDIR, "humi1.rrd"), f"N:{humidity}")
    sensor_graph(os.path.join(INITDIR, "temp1"),"temp")
    sensor_graph(os.path.join(INITDIR, "humi1"),"humi")
    return temp, humi


def display_data(temp, humi):
    """ Display sensor data and time on 14 segment, 4 digit display.
    """

    # Configure immediately before display, otherwise empty display is shown
    i2c = board.I2C()
    display = segments.Seg14x4(i2c, address=0x70)
    display.brightness = 0.5

    display.print("TIME")
    time.sleep(2)
    local_time = time.strftime("%H.%M", time.localtime())
    display.print(local_time)
    time.sleep(13)

    display.print("TEMP")
    time.sleep(2)
    display.print("    ")
    display.print(f"{temp:>4}")
    time.sleep(13)

    display.print("TIME")
    time.sleep(2)
    local_time = time.strftime("%H.%M", time.localtime())
    display.print(local_time)
    time.sleep(13)

    display.print("HUMI")
    time.sleep(2)
    display.print("    ")
    display.print(f"{humi:>4}")
    # Leave it blank, display stays on after the script ends



if __name__ == '__main__':

    INITDIR = os.path.dirname(__file__)

    try:
        # Prepare / read data
        tmp, hmi = read_data()

        # Display data on LED-backpack
        display_data(tmp, hmi)


    except KeyboardInterrupt:
        print("Script terminated by user!")

    except Exception as e:
        print("Unexpected error: %s", e)
