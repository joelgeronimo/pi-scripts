#!/usr/bin/sh

# Delete any previous entry of the backup config
rm -f /home/pi/Applications/teleporter/pi-hole-raspberrypi-teleporter_*

# Run the teleporter
pihole -a -t

# Move the generated file to the Applications folder
mv pi-hole-raspberrypi-teleporter_* /home/pi/Applications/teleporter/