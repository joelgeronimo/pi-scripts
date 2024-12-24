#!/usr/bin/sh

cd /home/pi/Applications/teleporter/ && rm -f pi-hole-raspberrypi-teleporter_* && /usr/local/bin/pihole -a -t &
