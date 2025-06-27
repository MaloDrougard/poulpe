import logging

# Configuration for webcam
deviceid = 4



# Configure for arduino
arduino_port = "/dev/ttyACM0"



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger("tentacule")