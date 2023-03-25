Hello!

This project is small project for temperature and humidity logging, with an Adafruit AM2315 sensor
(https://learn.adafruit.com/am2315-encased-i2c-temperature-humidity-sensor) and an Adafruit 0.54" Alphanumeric Backpack
(https://learn.adafruit.com/adafruit-led-backpack/0-54-alphanumeric).

The project folder contains some legacy code from my earlier implementation, as well as the implementation guide
from https://ismellsmoke.net/ (many thanks) and the modified code scripts from
SwitchDocLabs (https://github.com/switchdoclabs/SDL_Pi_AM2315). The latter code has been changed to work with python3.

The project has an RRD fabric script, which creates the databases for the logging, and a small script which is intended
to be used with Raspberry Pi crontab, running it in every minute. The script reads the sensor, and displays the time,
temprerature and humidity data continously.
