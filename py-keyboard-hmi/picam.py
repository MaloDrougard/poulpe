#!/usr/bin/env python3
from picamera2 import Picamera2

from myglobal import logger

import time
import sys
import cv2
import subprocess
import threading
import queue
from flask import Flask, request, jsonify



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


    def run(self):
        # Create threads for the web server and the camera preview
        web_api_thread = threading.Thread(target=capture.start_web_api, daemon=True)
        camera_thread = threading.Thread(target=capture.start_display_capture)

        # Start the threads
        web_api_thread.start()
        camera_thread.start()

        # Wait for the camera thread to finish (web server runs as a daemon)
        camera_thread.join()


    def start_web_api(self):
        app = Flask(__name__)

        @app.route('/api/filter1', methods=['POST'])
        def toggle_filter1():
            logger.info(request.json)
            filter1_enable = request.json.get('enabled', False)
            # Send the updated filter1 status to the queue
            logger.info("set filter1_enable {filter1_enable} in queue") 
            self.data_queue.put({'filter1': filter1_enable})
            
            return jsonify({'status': 'success', 'filter1':filter1_enable})

        @app.route('/api/exit', methods=['POST'])
        def exit_app():
            logger.info("Exit request received")
            self.data_queue.put({'exit': True})
            return jsonify({'status': 'success', 'exit_requested': True})
            
        @app.route('/api/status', methods=['GET'])
        def get_status():
            return jsonify({'filter1': self.filter1})

        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)


    def start_display_capture(self):
        """
        """
        
        picam = self._setupcapture()
        picam.start()
        
        cv2.namedWindow("Picamera2 Preview", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Picamera2 Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        f1 = False
        exit_requested = False
        while True:
            frame = picam.capture_array()

            # Check if there is new data in the queue
            while not self.data_queue.empty():
                data = self.data_queue.get()
                logger.info(f"data in queue {data}")
                if 'filter1' in data:
                    f1 = data['filter1']  # Update filter1 status
                if 'exit'in data:
                    exit_requested = data['exit']
                    
            if f1:
                frame = self.filter1(frame)
            if exit_requested:
                break
            
            cv2.imshow("Picamera2 Preview", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        picam.stop()
        cv2.destroyAllWindows()
        

    def _setupcapture(self):
        width, height = getScreenWidthAndHeight()
        picam = Picamera2()
        config = picam.create_preview_configuration(
            main={"size": (width, height)},
            controls={"FrameDurationLimits": (33333, 33333)}  # lock to ~30 FPS (microseconds)
        )
        picam.configure(config)
        return picam


    def filter1(self, frame):
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return bgr


        





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
   