#!/bin/bash

/bin/mount -t nfs 192.168.31.32:/volume1/Plex /home/pi/Videos/Plex -o nolock,async,noatime,nodiratime,noexec,rw,nosuid

/bin/mount -t nfs 192.168.31.32:/volume1/Downloads /home/pi/Downloads/NAS -o nolock,async,noatime,nodiratime,noexec,rw,nosuid

/bin/mount -t nfs 192.168.31.32:/volume1/Backups /home/pi/Backups -o nolock,async,noatime,nodiratime,noexec,rw,nosuid
