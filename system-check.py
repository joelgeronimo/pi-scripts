import os
import psutil
import schedule
import time
import logging
from logging.handlers import TimedRotatingFileHandler


# Application constants
MAX_SWAP_PERCENTAGE = 70.0
MAX_CPU_LOAD_AVERAGE = 90.0
TASK_INTERVAL_MINUTES = 15
CPU_LOAD_AVERAGE_INDEX = 2 # (1 min, 5 min, 15 min) = psutil.getloadavg()

# Logger constants
LOGGER = "systemchecklog"
LOG_LEVEL = "DEBUG"
LOG_PATH = "/home/pi/Applications/logs/systemcheck.log"
LOG_WHEN = "d"
LOG_INTERVAL = 1
LOG_BACKUP_COUNT = 3


def reboot():
    os.system("sudo shutdown -r now")


def system_check():
    logger = logging.getLogger(LOGGER)
    
    # Retrieve system swap memory utilization
    swap_utilization = psutil.swap_memory()
    
    # Retrieve average CPU load
    cpu_load_avg = (psutil.getloadavg()[CPU_LOAD_AVERAGE_INDEX] / psutil.cpu_count()) * 100
    
    # Check swap percentage
    logger.info("Current swap percentage: {}".format(swap_utilization.percent))
    # If the swap percentage >= MAX_SWAP_PERCENTAGE, trigger a system reboot
    if swap_utilization.percent >= MAX_SWAP_PERCENTAGE:
        logger.info("Swap utilization exceeded {}. Rebooting pi...".format(MAX_SWAP_PERCENTAGE))
        reboot()
    
    # Check CPU load
    logger.info("CPU load average ({} min): {:.2f}".format(TASK_INTERVAL_MINUTES, cpu_load_avg))
    # If the average CPU load in the last N minutes >= MAX_CPU_LOAD_AVERAGE, trigger a system reboot
    if cpu_load_avg >= MAX_CPU_LOAD_AVERAGE:
        logger.info("CPU load average exceeded {}. Rebooting pi...".format(MAX_CPU_LOAD_AVERAGE))
        reboot()


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

    # Set the system check frequency
    schedule.every(TASK_INTERVAL_MINUTES).minutes.do(system_check)

    logger.info("System check script is now running!")
    while True:
        schedule.run_pending()
        time.sleep(1)
