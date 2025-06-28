import cv2

def capture2fullscreen(deviceid = 4): 
        
    # Open the webcam (0 is usually the default webcam)
    cap = cv2.VideoCapture(deviceid)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()


    # Set MJPG codec
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # Set resolution and FPS
    desired_width =  1920 #1280 # Set your desired width
    desired_height = 1080 #720   # Set your desired height
    desired_fps = 30      # Set your desired FPS

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
    cap.set(cv2.CAP_PROP_FPS, desired_fps)

    # Verify the settings
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"Camera resolution: {actual_width}x{actual_height}")
    print(f"Camera FPS: {actual_fps}")

    # Set fullscreen window
    cv2.namedWindow("Webcam", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display the frame
        cv2.imshow("Webcam", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture2fullscreen()