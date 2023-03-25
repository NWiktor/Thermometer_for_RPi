Hello!

This is a small project for temperature and humidity logging and displaying, with an Adafruit AM2315 sensor
(https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor) and an Adafruit 0.54" Alphanumeric Backpack
(https://learn.adafruit.com/adafruit-led-backpack/0-54-alphanumeric) for Raspberry Pi.

The project folder contains some legacy code from my earlier implementation (from 2018), as well as the latest guide
from Sopwith (https://ismellsmoke.net/) - many thanks - and last, but not least, the modified code scripts from
SwitchDocLabs (https://github.com/switchdoclabs/SDL_Pi_AM2315). The latter code has been changed to work with python3 according
to the .pdf guide.

The project has an RRD fabric script, which creates the databases for the logging, and a small script which is intended
to be used with Raspberry Pi crontab, running it in every minute. The script reads the sensor data, and displays the time,
temprerature and humidity data continously.
