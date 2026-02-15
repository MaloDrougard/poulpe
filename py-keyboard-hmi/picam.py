#!/usr/bin/env python3
from picamera2 import Picamera2

import time
import sys
import cv2

def preview():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (1920, 1080)},
        controls={"FrameDurationLimits": (33333, 33333)}  # lock to ~30 FPS (microseconds)
    )
    picam2.configure(config)
    picam2.start()

    try:
        while True:
            frame = picam2.capture_array()
            
            bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # apply bilateral filter (uses sigmaColor)
            bgr = cv2.bilateralFilter(bgr, d=9, sigmaColor=75, sigmaSpace=75)
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            # edge detection using Canny
            cv2.imshow("Picamera2 Preview", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        pass
    
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
  

if __name__ == "__main__":
    preview()