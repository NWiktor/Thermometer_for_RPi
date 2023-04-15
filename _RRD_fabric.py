# -*- coding: utf-8 -*-
# Létrehozza a szenzor adatsorokhoz tartozó RRD adatbázisokat, azok típusától függően.
import os
import rrdtool
import time
import sys


def create(filename, rrd_type):
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
        file_object=open(os.path.join(INITDIR, LOG),"a")
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        file_object.write(localtime + ": RRD nem hozható létre: ismeretlen típus!" + "\n")
        file_object.close()
        return

    # Létrehozás logolva
    file_object=open(os.path.join(INITDIR, LOG),"a")
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    file_object.write(localtime + ": Round robin adatbázis (RRD) létrehozva a " + filename + " helyen." + "\n")
    file_object.close()


def info(filename):
    print(rrdtool.info(filename))


if __name__ == "__main__":
    # Configure before creation!
    sensor1 = "temp1"
    sensor2 = "humi1"
    LOG = "RRD_log.txt"

    INITDIR = os.path.dirname(__file__)
    rrd_filename1 = os.path.join(INITDIR, sensor1, ".rrd")
    create(rrd_filename1, "temp")
    rrd_filename2 = os.path.join(INITDIR, sensor2, ".rrd")
    create(rrd_filename2, "humi")
