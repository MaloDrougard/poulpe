import logging
from logging.handlers import SysLogHandler
import platform
import os
from pathlib import Path

# Configuration for webcam
deviceid = 4

# Configure for arduin
def arduino_port():
    system = platform.system()
    if system == "Windows":
        logger.info("Choosing window config for arduino port")
        return "COM6"
    else:
        logger.info(f"Choosing linux config for arduino port")
        return "/dev/ttyACM0"


def partition_folder(): 
    return Path(__file__).resolve().parent / "partitions"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger("poulpe")
syslog_handler = SysLogHandler(address = '/dev/log')
syslog_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(syslog_handler)


def display_api(): 
    return "http://localhost:5000"