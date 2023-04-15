#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This script creates an RRD database depending on harcoded types.
Wetzl Viktor - 2023.03.25
"""

# pylint: disable = import-error
import os
import time
import rrdtool


def create(filename, rrd_type):
    """  """
    if rrd_type == "temp":
        # Adott hőmérséklet adatsorhoz.
        # RRD létrehozása, 60 s lépésközzel, azonnali kezdéssel
        rrdtool.create(filename, "--step", "60", "--start", "now", #"--no-overwrite",
        "DS:temp:GAUGE:150:-40:80", #150s-ig várja az adatot, -40 és +80 között
        "RRA:AVERAGE:0.5:1:10080", #Percenkénti "átlag", egy hétre
        "RRA:AVERAGE:0.5:30:1440", #Fél óránkénti átlag, egy hónapra
        "RRA:AVERAGE:0.5:1440:366", #Napi átlag, egy évre
        "RRA:MIN:0.5:1440:366", #Napi min., egy évre
        "RRA:MAX:0.5:1440:366") #Napi max., egy évre

    elif rrd_type == "humi":
        # Adott páratartalom adatsorhoz.
        # RRD létrehozása, 60 s lépésközzel, azonnali kezdéssel
        rrdtool.create(filename, "--step", "60", "--start", "now", #"--no-overwrite",
        "DS:humi:GAUGE:150:0:100", #150s-ig várja az adatot, 0 és 100 között
        "RRA:AVERAGE:0.5:1:10080", #Percenkénti "átlag", egy hétre
        "RRA:AVERAGE:0.5:30:1440", #Fél óránkénti átlag, egy hónapra
        "RRA:AVERAGE:0.5:1440:366", #Napi átlag, egy évre
        "RRA:MIN:0.5:1440:366", #Napi min., egy évre
        "RRA:MAX:0.5:1440:366") #Napi max., egy évre

    else:
        with open(os.path.join(INITDIR, LOG),"a", encoding="utf8") as file_object:
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            file_object.write(f"{localtime}: RRD nem hozható létre: ismeretlen típus!\n")
        return

    # Létrehozás logolva
    with open(os.path.join(INITDIR, LOG),"a", encoding="utf8") as file_object:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        file_object.write(f"{localtime}: RRD létrehozva a {filename} helyen.\n")


def info(filename):
    """  """
    print(rrdtool.info(filename))


if __name__ == "__main__":
    # Configure before creation!
    SENSOR1 = "temp1"
    SENSOR2 = "humi1"
    LOG = "RRD_log.txt"

    INITDIR = os.path.dirname(__file__)
    rrd_filename1 = os.path.join(INITDIR, SENSOR1, ".rrd")
    create(rrd_filename1, "temp")
    rrd_filename2 = os.path.join(INITDIR, SENSOR2, ".rrd")
    create(rrd_filename2, "humi")
