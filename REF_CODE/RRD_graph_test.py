# -*- coding: utf-8 -*-
import rrdtool
import time


def sensor_graph(graph_filename, rrd_filename, rrd_type):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    if rrd_type == "temp":
        rrdtool.graph(graph_filename,
        "-v", "Hőmérséklet [°C]",
        "-t", "Idő [s]",
        "-e", "now",
        "-s", "e-24h",
        #"-S", "300",
        "-w", "1600",
        "-h", "800",
        "-u", "45",
        "-l", "0",
        #"-g", # No legend
        "-n", "DEFAULT:10:Arial", # Font
        "-W", "Wetzl Viktor @ " + localtime,
        #/home/viktor/HAS/temp1.rrd
        "DEF:ds01={0}:temp:AVERAGE".format(rrd_filename),
        "AREA:ds01#3399FF", #60% kék
        "LINE2:ds01#004D99") # 40% kék


if __name__ == "__main__":
    sensor1 = "test1"
    sensor_graph("/home/viktor/HAS/{0}.png".format(sensor1),"/home/viktor/HAS/temp1.rrd".format(sensor1),"temp")
