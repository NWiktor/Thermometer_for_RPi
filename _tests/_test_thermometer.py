#!/usr/bin/env python3

import board
from adafruit_ht16k33 import segments
import AM2315
import time
import os
import traceback
import rrdtool

thsen = AM2315.AM2315(powerpin=6)
i2c = board.I2C()
display = segments.Seg14x4(i2c, address=0x70)
display.brightness = 0.5
# display.blink_rate = 3
# display.print("ABCD")
# display.print(1234)
# display.print_hex(0x1A2B)
# display[0] = '1'
# display[1] = '2'
# display[2] = 'A'
# display[3] = 'B'
# display.marquee('This is a really long string ', 0.5, False)


def sensor_graph(graph_filename, rrd_filename, rrd_type):
    # Grafikon generálása az RRD adatok alapján, szenzor típusától függően.
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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
        "-W", "Wetzl Viktor @ " + localtime,
        "DEF:ds01={0}:temp:AVERAGE".format(rrd_filename),
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
        "-u", "100",
        "-l", "0",
        "--allow-shrink",
        #"-g", # No legend
        "-n", "DEFAULT:10:Arial", # Font
        "-W", "Wetzl Viktor @ " + localtime,
        "DEF:ds01={0}:humi:AVERAGE".format(rrd_filename),
        "AREA:ds01#75FF33", #60% zöld
        "LINE2:ds01#41CC00") # 40% zöld


if __name__ == '__main__':
    try:
        display.marquee('INITIALIZING    ', 0.5, False)

        while True:
            # localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            localtime = time.strftime("%H.%M", time.localtime())
            h, t = thsen.read_humidity_temperature()
            temperature = str("{:3.1f}".format(t))
            humidity = str("{:3.1f}".format(h))
            rrdtool.update("/home/viktor/SDL_Pi_AM2315/temp1.rrd", "N:{0}".format(temperature))
            rrdtool.update("/home/viktor/SDL_Pi_AM2315/humi1.rrd", "N:{0}".format(humidity))
            print("Data read from sensor!")

            # Szenzor chartok generálása
            sensor_graph("/home/viktor/SDL_Pi_AM2315/temp1.png","/home/viktor/SDL_Pi_AM2315/temp1.rrd","temp")
            sensor_graph("/home/viktor/SDL_Pi_AM2315/humi1.png","/home/viktor/SDL_Pi_AM2315/humi1.rrd","humi")
            print("Graphs updated!")
           
            display.print("TIME")
            time.sleep(2)
            display.print("    ")
            display.print(localtime)
            time.sleep(18)

            display.print("TEMP")
            time.sleep(2)
            display.print("    ")
            display.print("{:>4}".format(t))
            time.sleep(18)

            display.print("HUMI")
            time.sleep(2)
            display.print("    ")
            display.print("{:>4}".format(h))
            time.sleep(18)

    except KeyboardInterrupt:
        print("Script terminated!")

    finally:
        display.marquee('TURNING OFF', 0.5, False)
        display.print("    ")
