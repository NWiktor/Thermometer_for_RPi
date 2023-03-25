# -*- coding: utf-8 -*-
# A szenzorok adatainak kiolvasását, RRD adatbázisba töltését és a grafikon generálását végzi.
import time
import Adafruit_DHT
import HAS_aosong_sensor as HAS_AS
import HAS_message_control as mc
import rrdtool


def sensor_reading():
    sensor_data1 = []
    sensor_data2 = []

    # -- DHT22 --
    # 0-100% humidity readings with 2-5% accuracy
    # -40 to 80°C temperature readings ±0.5°C accuracy
    sensor = Adafruit_DHT.DHT22 # A DHT 22 szenzor van beépítve.
    pin = "12" # A 12-es pinen van bekötve a szenzor.

    # Try to grab a sensor reading. Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    tup = Adafruit_DHT.read_retry(sensor, pin)
    # sorrend: humidity, temperature
    sensor_data1.append(tup[0])
    sensor_data1.append(tup[1])

    # Az adatok nem mindig kiolvashatóak (Linux rendszer sajátosság)
    if sensor_data1[0] is None:
        mc.error("Error occured when readig out of DHT22 sensor, humidity data!")

    elif sensor_data1[1] is None:
        mc.error("Error occured when readig out of DHT22 sensor, temperature data!")

    else:
        pass

    # -- AOSONG --
    # Reads the Aosong sensor temperature and humidity data, then calculates dewpoint
    # If error occures, retry 5 times, with 1 sec interval
    for n in range(1,6):
        try:
            humi, temp, dew = HAS_AS.main(info=False);

        except AssertionError, e:
            # Lefut, ha assertion error-ra fut a kiolvasás
            mc.debug("Assertion error when readout of AOSONG sensor! Iteration nr. {0}".format(n))

            if n == 5:
                mc.error("Error occured when readout of AOSONG sensor!")
                break

            else:
                time.sleep(1)
                continue

        else:
            # Lefut, ha nincs exception; kilép a for loop-ból
            sensor_data2.append(humi)
            sensor_data2.append(temp)
            sensor_data2.append(dew)
            mc.debug("Script exited from loop.")
            break


    sensor_data = sensor_data1 + sensor_data2
    mc.debug("Sensor reading finished!")
    return sensor_data[0], sensor_data[1], sensor_data[2], sensor_data[3]


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
        "-u", "45",
        "-l", "0",
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
        #"-g", # No legend
        "-n", "DEFAULT:10:Arial", # Font
        "-W", "Wetzl Viktor @ " + localtime,
        "DEF:ds01={0}:humi:AVERAGE".format(rrd_filename),
        "AREA:ds01#75FF33", #60% zöld
        "LINE2:ds01#41CC00") # 40% zöld

    else:
        mc.error("Graph is not generateable: unknown RRD type: {0}!".format(rrd_type))


def main():
    #Szenzor adatok kiolvasása
    humidity, temperature, humidity2, temperature2 = sensor_reading()

    #Szenzor adatok formázása
    temperature = str("{:3.1f}".format(temperature))
    humidity = str("{:3.1f}".format(humidity))
    temperature2 = str("{:3.1f}".format(temperature2))
    humidity2 = str("{:3.1f}".format(humidity2))
    mc.debug("Sensor data formatted.")

    try:
        #Adatok tárolása RRD adatbázisban
        rrdtool.update("/home/viktor/HAS/{0}.rrd".format(sensor1), "N:{0}".format(temperature))
        rrdtool.update("/home/viktor/HAS/{0}.rrd".format(sensor2), "N:{0}".format(humidity))
        rrdtool.update("/home/viktor/HAS/{0}.rrd".format(sensor3), "N:{0}".format(temperature2))
        rrdtool.update("/home/viktor/HAS/{0}.rrd".format(sensor4), "N:{0}".format(humidity2))

    except Exception as e:
        # Jogosultsági és I/O hibák elkapása
        mc.error(e.message)

    # Ideiglenes tárolóba írja a szenzoros adatokat
    file_object=open("/home/viktor/HAS/Buffer.txt","w")
    file_object.write(temperature + "\n")
    file_object.write(humidity + "\n")
    file_object.write(temperature2 + "\n")
    file_object.write(humidity2 + "\n")
    file_object.close()
    mc.debug("Buffer writing completed.")

    # Szenzor chartok generálása
    sensor_graph("/home/viktor/HAS/{0}.png".format(sensor1),"/home/viktor/HAS/{0}.rrd".format(sensor1),"temp")
    sensor_graph("/home/viktor/HAS/{0}.png".format(sensor2),"/home/viktor/HAS/{0}.rrd".format(sensor2),"humi")
    sensor_graph("/home/viktor/HAS/{0}.png".format(sensor3),"/home/viktor/HAS/{0}.rrd".format(sensor3),"temp")
    sensor_graph("/home/viktor/HAS/{0}.png".format(sensor4),"/home/viktor/HAS/{0}.rrd".format(sensor4),"humi")
    mc.debug("Sensor charts sucessfully generated.")


# Main script
sensor1 = "temp1"
sensor2 = "humi1"
sensor3 = "temp2"
sensor4 = "humi2"

try:
    mc.debug("Sensor logging started.")
    main()

except:
    mc.error("HAS_sensor_logger.py script stopped unexpectedly!")

finally:
    pass
    mc.debug("Script finished running!")
