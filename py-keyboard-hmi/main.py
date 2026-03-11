import myglobal
from myglobal import logger
import arduinocomm
import threading
import webcam
import picam 
import midi
import arduino_restapi

#import keyboard
#import mykeyboard


logger.info("start")

# setup the arduino serial connection
#arduinocomm.setup()

# start READ from serial in a separate thread 
# write is done directly by the other process
# logger.info("start arduino communication")
# serial_thread = threading.Thread(target=arduinocomm.read_from_serial, daemon=True)
# serial_thread.start()

# # capture the webcam and display on the sceen.
# logger.info("start video capture")
# serial_thread = threading.Thread(target=webcam.capture2fullscreen, args=(myglobal.deviceid,), daemon=True)
# serial_thread.start()

# listen to midi inputs and call the apropriate apis 
logger.info("start listen to midi inputs")
midi_thread = threading.Thread(target=midi.listen_midis, daemon=True)
midi_thread.start()

# Run arduino REST API in a background thread
logger.info(f"start Arduino REST API in background thread")
arduino_api_thread = threading.Thread(
        target=arduino_restapi.run_api,
        args=("0.0.0.0", 5001),
        daemon=True
    )
arduino_api_thread.start()
    

# capture the webcam and display on the sceen.
cam2monitor_thread = picam.Capture2FullscreenWithRestApi()
cam2monitor_thread.run()




# # setup the keybinding 
# logger.info("start keyboard capture")
# mykeyboard.setup() # directly start to listen to event
# keyboard.wait('q') # loop until 'q' is recieved

logger.info('exiting')
arduinocomm.setdown()