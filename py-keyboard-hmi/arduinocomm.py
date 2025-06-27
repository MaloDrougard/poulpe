import serial
import time
import threading
import myglobal
from myglobal import logger


# Configure the serial connection
arduino_port = '/dev/ttyACM0'  # Replace with your Arduino's port
if myglobal.arduino_port:
    arduino_port = myglobal.arduino_port

baud_rate = 115200  # Match the baud rate set in your Arduino sketch

sleep_read = 0.01
sleep_write = 0.1

ser = None

def setup():
    
    global ser # to set it up globaly 
    
   # Initialize serial connection
    logger.info(f"Initializing serial connection on port {arduino_port}...")
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.reset_input_buffer()


def setdown():
    global ser
    if ser:
        ser.close()    


def read_from_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            logger.info(f"ARDUINO: {data}")
        time.sleep(sleep_read)
        

def send_cmd(command: str):
    ser.write((command + '\n').encode('utf-8'))
    logger.info(f"Sent command: {command}")
    

if __name__ == "__main__":
    setup()
    read_from_serial()
