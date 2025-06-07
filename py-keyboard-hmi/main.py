from myglobal import logger
import arduinocomm
import mykeyboard
import threading
import keyboard

logger.info("start")

# setup the arduino serial connection
arduinocomm.setup()

# start read from serial in a separate thread 
serial_thread = threading.Thread(target=arduinocomm.read_from_serial, daemon=True)
serial_thread.start()

# setup the keybinding 
mykeyboard.setup() # directly start to listen to event
keyboard.wait('q') # loop until 'q' is recieved

logger.info('exiting')
arduinocomm.setdown()