import os
import time
import schedule
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

SOURCE = "/home/pi/Applications/"
EMBY_SOURCE = "/var/lib/emby"
PIHOLE_TELEPORTER_DESTINATION = "/home/pi/Applications/teleporter/"
DESTINATION = "/home/pi/Backups/RPi/"
RETENTION = 3
DATE_FORMAT = "%Y%m%d"
RUN_EVERY_DAY_AT = "04:00"

# Logger constants
LOGGER = "backuplog"
LOG_LEVEL = "DEBUG"
LOG_PATH = "/home/pi/Applications/logs/backup.log"
LOG_WHEN = "d"
LOG_INTERVAL = 1
LOG_BACKUP_COUNT = 2


def backup():
    logger = logging.getLogger(LOGGER)
    create_new_backup = True
    backup_dates = []
    current_date = datetime.today()

    # List the current backup folders
    for dirs in os.listdir(DESTINATION):
        old_backup = os.path.join(DESTINATION, dirs)
        if os.path.isdir(old_backup):
            logger.info("Old backup folder: {}".format(dirs))
            # Get the date value of the folder and append to the list
            old_date = datetime.strptime(dirs, DATE_FORMAT)
            backup_dates.append(old_date)
            if old_date.strftime(DATE_FORMAT) == current_date.strftime(DATE_FORMAT):
                create_new_backup = False

    # Sort the dates
    backup_dates_sorted = sorted(backup_dates)

    # Check the retention
    backup_dates_sorted_len = len(backup_dates_sorted)
    if backup_dates_sorted_len >= RETENTION:
        # The number of backups exceed the set retention. Delete as necessary.
        # We add 1 to the sorted len to allocate the space for the new backup folder.
        num_delete = (backup_dates_sorted_len + 1) - RETENTION
        for x in range(num_delete):
            # Pop the first element in the list
            backup_to_delete = backup_dates_sorted.pop(0).strftime(DATE_FORMAT)
            # Delete
            logger.info("Deleting backup folder due to retention: {}".format(backup_to_delete))
            p = subprocess.run(["rm", "-rf", os.path.join(DESTINATION, backup_to_delete)], stdout=subprocess.PIPE)

    if create_new_backup:
        # Create a new backup folder
        new_backup = os.path.join(DESTINATION, current_date.strftime(DATE_FORMAT))
        inside_new_backup = os.path.join(new_backup, "")
        if not os.path.exists(new_backup):
            logger.info("Creating new backup folder: {}".format(new_backup))
            os.makedirs(new_backup)

        # Perform pi-hole config backup using teleporter
        p = subprocess.run("ls {}".format(PIHOLE_TELEPORTER_DESTINATION), shell=True, stdout=subprocess.PIPE)
        old_teleporter_config = p.stdout.decode("utf-8").strip("\n").split("\n")[0]
        if len(old_teleporter_config) > 0:
            # Delete the old config
            logger.info("Deleting old teleporter config: {}".format(old_teleporter_config))
            p = subprocess.run("rm -f {}{}".format(PIHOLE_TELEPORTER_DESTINATION, old_teleporter_config), shell=True, stdout=subprocess.PIPE)
        # Run the teleporter
        p = subprocess.run(["pihole", "-a", "-t"], stdout=subprocess.PIPE)
        p = subprocess.run("ls pi-hole-raspberrypi-teleporter_*", shell=True, stdout=subprocess.PIPE)
        new_teleporter_config = p.stdout.decode("utf-8").strip("\n").split("\n")[0]
        logger.info("New teleporter config: {}".format(new_teleporter_config))
        p = subprocess.run(["mv", new_teleporter_config, PIHOLE_TELEPORTER_DESTINATION], stdout=subprocess.PIPE)

        # Perform the RSYNC and place it in the new backup folder
        logger.info("Performing rsync...")
        p = subprocess.run(["rsync", "-rz", SOURCE, new_backup], stdout=subprocess.PIPE)

        # Perform the RSYNC for Emby folder, placing it inside the new backup folder
        p = subprocess.run(["rsync", "-rz", EMBY_SOURCE, inside_new_backup], stdout=subprocess.PIPE)

        logger.info("rsync done.")
    else:
        logger.info("Backup folder already exists, rsync skipped.")


if __name__ == "__main__":
    logger = logging.getLogger(LOGGER)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    handler = TimedRotatingFileHandler(LOG_PATH,
                                       when=LOG_WHEN,
                                       interval=LOG_INTERVAL,
                                       backupCount=LOG_BACKUP_COUNT)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set the backup frequency
    schedule.every().day.at(RUN_EVERY_DAY_AT).do(backup)

    logger.info("Backup script is now running!")
    while True:
        schedule.run_pending()
        time.sleep(1)
