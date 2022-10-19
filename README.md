# pi-scripts
**A collection of python code that does something useful.**

pi-scripts is my attempt to collate my personal work that was created to maximize and maintain a Raspberry pi 3B+.

## Scripts

- [backup](#backup)
- [system-check](#system-check)

### backup
Since I had the unfortunate incident of an SD card failing on a previous build, it dawned on me the monumental task of trying to recall and replicate configurations for my installed applications. Since these settings constantly change, I created this script to completely copy and backup my whole `Applications` folder which contains the configurations files installed on the pi. Not all settings are saved on this folder though, at least for now. So if in case disaster does strike, I would not be starting completely from scratch.

The script creates a folder to an NFS mounted folder on the pi with a naming convention of `YYYYMMDD`. It utilizes `rsync` to copy the entire `Applications` folder to that newly created folder. The script then checks the allowed number of copies. If if exceeds the retention, it deletes the oldest version.

This task is scheduled to run every Sunday at 21:00.

This script is added on crontab (as user pi) `crontab -e`, then add the following line:
```sh
@reboot sleep 20; python3 /home/pi/Applications/backup.py &
```

### system-check
This script was born out of necessity. As the number of running docker containers increased, maintaining a healthy and free swap space became one of the solutions to avoid the pi from freezing. If that was not enough, I added a check on the average CPU load (on 5 minute intervals) as well, to verify if there are ghost applications consuming too much CPU cycles (as this has happened before: I cannot stop the deluge container).

Therefore, if any of those 2 conditions were met, the pi would reboot.

You may want to avert your eyes on the usage of the `os.system("sudo shutdown -r now")` LOL.

This task is scheduled to run every 5 minutes.

This script is added on crontab (as user pi) `crontab -e`, then add the following line:
```sh
@reboot sleep 20; python3 /home/pi/Applications/system-check.py &
```