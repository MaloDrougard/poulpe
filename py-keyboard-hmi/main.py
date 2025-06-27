import myglobal
from myglobal import logger
import arduinocomm
import mykeyboard
import threading
import keyboard
import webcam

logger.info("start")

# setup the arduino serial connection
arduinocomm.setup()

# start read from serial in a separate thread 
logger.info("start arduino communication")
serial_thread = threading.Thread(target=arduinocomm.read_from_serial, daemon=True)
serial_thread.start()

# capture the webcam and display on the sceen.
logger.info("start video capture")
serial_thread = threading.Thread(target=webcam.capture2fullscreen, args=(myglobal.deviceid,), daemon=True)
serial_thread.start()

# setup the keybinding 
logger.info("start keyboard capture")
mykeyboard.setup() # directly start to listen to event
keyboard.wait('q') # loop until 'q' is recieved

logger.info('exiting')
arduinocomm.setdown()