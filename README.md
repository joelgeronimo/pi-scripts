# pi-scripts
**A collection of python code that does something useful.**

pi-scripts is my attempt to collate my personal work that was created to maximize and maintain a Raspberry pi 3B+.

## Scripts

- [system-check](#system-check)

### system-check
This script was born out of necessity. As the number of running docker containers increased, maintaining a healthy and free swap space became one of the solutions to avoid the pi from freezing. If that was not enough, I added a check on the average CPU load (on 5 minute intervals) as well, to verify if there are ghost applications consuming too much CPU cycles (as this has happened before: I cannot stop the deluge container).

Therefore, if any of those 2 conditions were met, the pi would reboot.

You may want to avert your eyes on the usage of the `os.system("sudo shutdown -r now")` LOL.

This script is added on crontab (as user pi) `crontab -e`, then add the following line:
```sh
@reboot sleep 20; python3 /home/pi/Applications/system-check.py &
```