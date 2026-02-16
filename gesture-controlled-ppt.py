import cv2
import time #In order to measure how much time does each frame take

capture = cv2.VideoCapture(0) #This initializes the webcam, (0)means using the default camera, if we had multiple cameras, 1 or 2 would select others

previous_time = 0 #This will be storing the timestamps of the previous frames, at the start it will be 0 as we haven't measured anything

while True: #Every iteration = 1 frame from webcam
    ret, frame = capture.read() #Ret is the boolean value that indicates wheather the frame is successfully read and captured 
    #Frame is the actual image that was captured

    if not ret: #If the boolean value is not read successfully
        print("Failed to grab frame")
        break

    current_time = time.time() #This gives current time in seconds

    fps = 1 / (current_time - previous_time) #current time - previous time gives the time taken for one frame
    #This line calculates the fps and the formula goes in like 1 / time per frame

    previous_time = current_time

    cv2.putText( #This is drawing FPS on the screen
        frame, f"FPS: { int(fps) }", (20, 40),  #20,40 is the position on the frame
        cv2.FONT_HERSHEY_SIMPLEX, 1, #Using the font
        (0, 255, 0), 2 #0,255,0 is the portraying the green colour (BGR format) and 2 is the thickness
    )

    cv2.imshow("Webcam Feed", frame) #This displays the frame in a window titled "Webcam Feed", right now this is the raw output feed

    if cv2.waitKey(1) & 0xFF == ord('q'): #Wait for 1 second and when pressed q, it breaks the loop
        break

capture.release() 
cv2.destroyAllWindows() #This destroys all the windows when the loop ends