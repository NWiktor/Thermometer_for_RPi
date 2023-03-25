# -*- coding: utf-8 -*-
import sys
import time
import HAS_solar_position as HAS_SP
import HAS_message_control as mc


# Main script
try:
    mc.debug("Script started.")
    reportpath = "/home/viktor/HAS/Twilight_report.txt"
    report_string = []
    twilight_deg = []
    twilight_LT = []

    # Geolokációs adatok
    geoloc = ["Budapest", 47.497912, 19.040235, 1.000000]

    # Aktuális dátum és időadatok kiolvasása
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Y, M, D = localtime.split(" ")[0].split("-")

    # Ha nyári időszámítás van érvényben
    if time.localtime().tm_isdst:
        tz = geoloc[3] + 1.0
        dst = " (DST)"

    else:
        tz = geoloc[3]
        dst = ""

    # Report header adatok készítése
    report_string.append(" -- DAILY TWILIGHT REPORT -- ")
    report_string.append(" -- {0} (UTC{1:+.0f}) -- ".format(geoloc[0], geoloc[3]))
    report_string.append(" -- {0}-{1}-{2} -- ".format(Y, M, D ))
    report_string.append("Location name: {0}".format(geoloc[0]))
    report_string.append("Latitude: {0}°".format(geoloc[1]))
    report_string.append("Longitude: {0}°".format(geoloc[2]))
    report_string.append("Timezone: UTC{0:+.0f}{1}".format(tz, dst))
    mc.debug("Report metadata is ready!")

    # Twilight időpontok számítása, és hozzáadás a reporthoz
    mc.debug("Calculating report results has been started.")
    date = HAS_SP.JD(int(Y), int(M), int(D), timezone=tz, info=False)
    rep_string = HAS_SP.twilight_times(date, geoloc[1], geoloc[2], timezone=tz, info=False)
    report_string += rep_string
    mc.debug("Report results are ready!")

    report_string.append(" --------------------------- ")
    report_string.append("Report generated at {} ".format(localtime))

    # Writing report to file
    mc.debug("Report writing to file started.")
    file_object=open(reportpath,"w")
    #localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for n in range(0,len(report_string)):
        file_object.write(report_string[n] + "\n")

    file_object.close()
    mc.debug("Report writing to file finished.")

except:
    mc.error("HAS_twilight_report.py script stopped unexpectedly!")

else:
    mc.info("Twilight report completed successfully!")
