import logging
import platform

# Configuration for webcam
deviceid = 4



# Configure for arduin
def arduino_port():
    system = platform.system()
    if system == "Windows":
        print("The laptop is running Windows.")
        return "COM6"
    else:
        print(f"The laptop is running {system}.")
        return "/dev/ttyACM0"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger("tentacule")