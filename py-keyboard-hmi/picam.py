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


class Transform():
    
    def __init__(self, messages: queue = None):
        
        self.brightness = 0
        self.hue = 0
        self.saturation = 1.0
        self.contrast = 1.0

        # message queue to recieve info from other THREAD
        self.messages = messages

    
    def start_display_capture(self):
        
        picam = self._setupcapture()
        picam.start()
        
        cv2.namedWindow("Picamera2 Preview", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Picamera2 Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        while True:
            
            # Parse message in qeue and set the properties of the filter/object
            self.parse_messages_queue()
            
            # return rgb image 
            rgb = picam.capture_array()
            
            # Convert RGB to HSV
            hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)        
            
            hsv = self.filter_brightness_hue_saturation(hsv, self.brightness, self.hue, self.saturation)
            hsv = self.filter_contrast(hsv, self.contrast)           
           
            # Convert HSV to BGR before displaying
            bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            cv2.imshow("Picamera2 Preview", bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        picam.stop()
        cv2.destroyAllWindows()
    

        
    def parse_messages_queue(self):
        if not self.messages:
            return 
        
        while not self.messages.empty():
            data = self.messages.get()
            logger.info(f"data in queue {data}")
            if 'filter' in data:
                if data['filter'] == 1:
                    self.brightness = int((data.get('value', 63) - 63) * 200 / 128)
                elif data['filter'] == 2:
                    self.hue = int((data.get('value', 63) - 63) * 180 / 128)
                elif data['filter'] == 3:
                    self.saturation = data.get('value', 63) / 64.0
                elif data['filter'] == 4:
                    self.contrast = data.get('value', 63) / 64.0
        

    def _setupcapture(self):
        width, height = getScreenWidthAndHeight()
        picam = Picamera2()
        config = picam.create_preview_configuration(
            main={"size": (width, height)},
            controls={"FrameDurationLimits": (33333, 33333)}  # lock to ~30 FPS (microseconds)
        )
        picam.configure(config)
        return picam

    
    def filter_contrast(self, frame, contrast=1.0):
        """
        Apply contrast adjustment to frame.
        
        Args:
            frame: Input frame in HSV format
            contrast: Contrast multiplier (0.0 to 2.0)
        """
        hsv = frame.astype(float)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * contrast, 0, 255)
        return hsv.astype('uint8')
    
       
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
    
    


class Capture2Fullscreen():
    """
    Capture the a raspberry camera input, transform it and display it fullscreen.
    The control of the transformation is done via a web REST interface. 
    Thus two threads are started once for the web interface and one for the capture and display. 
     
        Usage: 
            capture = Capture2Fullscreen()
            capture.run()
        
        The rest interface can be access as:
        curl -X POST -H "Content-Type: application/json" -d '{"enabled": true}' http://localhost:5000/api/filter1 {"filter1":true,"status":"success"}

    """
    
    def __init__(self):
        self.data_queue = queue.Queue()  # Shared queue for communication
        self.transform = Transform(self.data_queue)
        

    def run(self):
        # Create threads for the web server and the camera preview
        web_api_thread = threading.Thread(target=self.start_web_api, daemon=True)
        camera_thread = threading.Thread(target=self.transform.start_display_capture)

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
    capture = Capture2Fullscreen()
    capture.run()
