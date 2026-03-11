#!/usr/bin/env python3
from picamera2 import Picamera2

from myglobal import logger, display_api

import time
import sys
import cv2
import subprocess
import threading
import queue
from flask import Flask, request, jsonify
import numpy as np  # Ensure NumPy is imported


class Capture2Fullscreen():
    
    def __init__(self, messages: queue = None):
        
        # message queue to recieve info from other THREAD
        self.messages = messages

        self.width = -1
        self.height = -1

        
        self.enable_hsb_filter = False
        self.hue = 0
        self.saturation = 1.0
        self.brightness = 0
        
        # RGB filter
        self.enable_rgb_filter = False
        self.red = 1.0
        self.green = 1.0
        self.blue = 1.0
        
        
        # variable for the function update_and_log_fps
        self.fps_counter = 0
        self.fps_start_time = -1
        self.fps_log_frequence = 4  # in second
    

    def start(self):
        
        picam = self._setupcapture()
        picam.start()
        
        window_name = "Poulpe"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
       
        while True:
            
            # Parse message in qeue and set the properties of the filter/object
            self.parse_messages_queue()
            
            # return rgb image 
            rgb = picam.capture_array()
            # Convert RGB to HSV
            hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
            
            
            if self.enable_hsb_filter: # self.enable_hsb_filter:    
                hsv = self.filter_brightness_hue_saturation(hsv, self.brightness, self.hue, self.saturation)
                   
            # Convert HSV to BGR before displaying
            bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            if self.enable_rgb_filter:
                bgr = self.filter_rgb(bgr, self.red, self.green, self.blue)
            
            cv2.imshow(window_name, bgr)
            
            # Calculate and display FPS
            self.update_and_log_fps()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        picam.stop()
        cv2.destroyAllWindows()
    

    def update_and_log_fps(self):
        """Update FPS counters and log once per second."""
        # initialise time if never set
        if self.fps_start_time == -1:
            self.fps_start_time = time.time()
            
        self.fps_counter += 1
        elapsed_time = time.time() - self.fps_start_time
        if elapsed_time >= self.fps_log_frequence:
            fps = self.fps_counter / elapsed_time
            logger.info(f"FPS: {fps:.2f}")
            # reset the value
            self.fps_start_time = time.time()
            self.fps_counter = 0
           
     
    def parse_messages_queue(self):
        """Process all messages in the queue and update filter settings."""
        if not self.messages:
            return 
        
        while not self.messages.empty():
            try:
                data = self.messages.get()
                logger.debug(f"data in queue {data}")
                
                action = data.get("action")
                if not action:
                    logger.warning(f"message without action received, msg: {data}")
                    continue
                
                if action == "set_value":
                    self._handle_set_value(data)
                elif action == "toggle_filter_group":
                    self._handle_toggle_filter(data)
                else:
                    logger.warning(f"unknown action: {action}")
                    
            except Exception as e:
                logger.error(f"Error processing message from queue: {e}")

    def _handle_set_value(self, data):
        """Handle set_value action for filter parameters."""
        filter_id = data.get('filter_id')
        value = data.get('value', 63)

        if filter_id == "brightness":
            self.brightness = int((value - 63) * 200 / 128)
        elif filter_id == "hue":
            self.hue = int((value - 63) * 180 / 128)
        elif filter_id == "saturation":
            self.saturation = value / 64.0
        elif filter_id == "red":
            self.red = value / 64.0
        elif filter_id == "green":
            self.green = value / 64.0
        elif filter_id == "blue":
            self.blue = value / 64.0
            
    def _handle_toggle_filter(self, data):
        """Handle toggle_filter_group action."""
        filter_group_id = data.get("filter_group_id")
        if filter_group_id == "hsb":
            self.enable_hsb_filter = not self.enable_hsb_filter
            logger.info(f"enable_hsb_filter set to: {self.enable_hsb_filter}")
        elif filter_group_id == "rgb":
            self.enable_rgb_filter = not self.enable_rgb_filter
            logger.info(f"enable_rgb_filter set to: {self.enable_rgb_filter}")

    def _setupcapture(self):
        
        width, height = getScreenWidthAndHeight()
        
        if self.width == -1:
            self.width = width
        if self.height == -1:
            self.height = height
            
        logger.info(f"width, height set to {self.width}, {self.height}")
        
        picam = Picamera2()
        config = picam.create_preview_configuration(
            main={"size": (self.width, self.height)},
            controls={"FrameDurationLimits": (33333, 33333)}  # lock to ~30 FPS (microseconds)
        )
        picam.configure(config)
        return picam

       
    def filter_brightness_hue_saturation(self, frame, brightness=0, hue=0, saturation=1.0):
        """
        Apply brightness, hue, and saturation adjustments to frame.
        
        Args:
            frame: Input frame in BGR format
            brightness: Brightness adjustment (-100 to 100)
            hue: Hue shift (0 to 180)
            saturation: Saturation multiplier (0.0 to 2.0)
        """
        
        logger.debug(f"brightness={brightness}, hue={hue}, saturation={saturation}")
        
        hsv = frame.astype(float)
        
        # Adjust hue
        hsv[:, :, 0] = (hsv[:, :, 0] + hue) % 180
        
        # Adjust saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        
        # Adjust brightness (value channel)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + brightness, 0, 255)
        
        # Convert back to BGR
        hsv = hsv.astype('uint8')
        return hsv
    
    
    def filter_invert_luminance(self, frame):
        """
        Invert the luminance (value channel) of the frame.
        
        Args:
            frame: Input frame in HSV format
        """
        hsv = frame.astype(float)
        hsv[:, :, 2] = 255 - hsv[:, :, 2]
        return hsv.astype('uint8')
    
    def filter_rgb(self, frame, red=1.0, green=1.0, blue=1.0):
        """
        Apply red, green, blue channel multipliers to a BGR frame.

        Args:
            frame: Input frame in BGR format
            red:   Red channel multiplier   (0.0 to 2.0, 1.0 = no change)
            green: Green channel multiplier (0.0 to 2.0, 1.0 = no change)
            blue:  Blue channel multiplier  (0.0 to 2.0, 1.0 = no change)
        """
        logger.debug(f"rgb filter: red={red}, green={green}, blue={blue}")

        bgr = frame.astype(float)

        # BGR order: channel 0 = Blue, 1 = Green, 2 = Red
        bgr[:, :, 0] = np.clip(bgr[:, :, 0] * blue,  0, 255)
        bgr[:, :, 1] = np.clip(bgr[:, :, 1] * green, 0, 255)
        bgr[:, :, 2] = np.clip(bgr[:, :, 2] * red,   0, 255)

        return bgr.astype('uint8')


class Capture2FullscreenWithRestApi():
    """
    Capture the a raspberry camera input, transform it and display it fullscreen.
    The control of this transformation is done via a web REST interface. 
    Thus two threads are started onc for the web interface and one for the capture and display. 
     
        Usage: 
            capture = Capture2FullscreenWithRestApi()
            capture.run()
        
        The rest interface can be access as:
        curl -X POST -H "Content-Type: application/json" -d '{"enabled": true}' http://localhost:5000/api/filter1 {"filter1":true,"status":"success"}

    """
    
    def __init__(self):
        self.data_queue = queue.Queue()  # Shared queue for communication
        self.transform = Capture2Fullscreen(self.data_queue)
        

    def run(self):
        # Create threads for the web server and the camera preview
        web_api_thread = threading.Thread(target=self.start_web_api, daemon=True)
        camera_thread = threading.Thread(target=self.transform.start)

        # Start the threads
        web_api_thread.start()
        camera_thread.start()

        # Wait for the camera thread to finish (web server runs as a daemon)
        camera_thread.join()


    def start_web_api(self):
        app = Flask(__name__)

        @app.route('/filter', methods=['POST'])
        def set_filter():
            logger.info(f"displayer-recieve: {request.json}")
            self.data_queue.put(request.json)
            return jsonify({'status': 'success'})

        @app.route('/exit', methods=['POST'])
        def exit_app():
            logger.info("Exit request received")
            
            self.data_queue.put({'exit': True})
            return jsonify({'status': 'success', 'exit_requested': True})
            
        @app.route('/status', methods=['GET'])
        def get_status():
            return jsonify({'filter1': self.filter1})

        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)



def getScreenWidthAndHeight():
    result = subprocess.run(['xrandr'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'connected' in line:
            resolution = line.split()[2].split('+')[0]
            width, height = map(int, resolution.split('x'))
            logger.info( f"resolution: {width}, {height}")
            return width, height



if __name__ == "__main__":
    capture = Capture2FullscreenWithRestApi()
    capture.run()
