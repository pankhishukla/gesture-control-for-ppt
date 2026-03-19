import cv2 #Used to access webcam 
import mediapipe as mp #Mediapipe is tool for hand detection and tracking
import time #Used for timing gestures
import pyautogui #This library allows us to trigger by interacting with the keyboard. Bascially it creates a fake 
import math #For the calculations

#Configuring the system
pyautogui.FAILSAFE = False #Prevents PyAutoGUI from stopping if the cursor reaches the corner of the screen
pyautogui.PAUSE = 0 #Removes the delay betweeen the mouse commands

screen_width, screen_height = pyautogui.size() #Screen size is required too map the finger position to the cursor position

pinch_threshold = 0.05 #This is the distance between the thumb and the index finger
click_threshold = 0.25 #This is quick pinching -> clicks
drag_threshold = 0.30 #This is longer pinching -> drags

#Initializing the variables
pinch_start_time = None
pinch_active = False
dragging = False

#For cursor smoothening
prev_x = 0
prev_y = 0

#Hand detection using Mediapipe
mp_hands = mp.solutions.hands #This contains a hand detection and a tracking model

hands = mp_hands.Hands( 
    static_image_mode = False, #This is us telling the mediapipe that we are not giving you the static images, we are giving you videos, this detects my hand one time and then in future it is faster to track with smoother tracking.
    #If it was true, it would have detected from the scratch

    max_num_hands = 1, #This just tracks one hand maximum, this is for faster and creates lesser confusion

    model_complexity = 1, #Mediapipe hasa different models, and this shows the medium model used

    min_detection_confidence = 0.7, #Mediapipe should be atleast 70% sure that it is showing a hand, if the confidence is lower, it will ignore 

    min_tracking_confidence = 0.7 #This is applied after the hand is detected, tracking means following the hand across the frames

) #Basically this only tells us where the hand is and where the hand joints are. Creates an object for hands and it will process each frame and detect hands   

mp_draw = mp.solutions.drawing_utils #This is used for marking landmarks and drawign connections on the hand


#This is setting up the camera
capture = cv2.VideoCapture(0) #This is accessing the webcam. 0 means the default camera output and 1,2 would be the external cameras

#This improves the camera resolution significantly
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #This is setting the width
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #This is setting the height

#Helper Functions
def cursor_position(index_finger):
    #This is converting the normalized finger coodinates (0, 1) to actual screen coordinates
    screen_x = int(index_finger.x * screen_width)
    screen_y = int(index_finger.y * screen_height)
    
    # pyautogui.moveTo(screen_x, screen_y, duration = 0.01) #This is to move the mouse to the finger position, duration adds micro smoothening

    #This function is to stop the cursor if it gets out of the window
    screen_x = max(1, min(screen_x, screen_width - 1))
    screen_y = max(1, min(screen_y, screen_height - 1))

    return screen_x, screen_y

def calculating_pinch_distance(index_finger, thumb):
    #This calculates the distance between the index finger and the thumb, and if the distance gets tooo less, it is seen as a click otherwise, it is a drag
    #Currently this is just the calculation

    distance = math.hypot(
        index_finger.x - thumb.x,
        index_finger.y - thumb.y 
    ) #This calculating the distance between the index finger and the thumb

    return distance

def handling_pinch(distance, screen_x, screen_y):
    #According to the pinch duration, this function determines if the gesture should trigger a click or a drag

    global pinch_active, pinch_start_time, dragging

    #If the pinch is detected
    if distance < pinch_threshold: #Fingers are too close, pinch is detected.
        if not pinch_active: #Indicates that the pinch has jsut started
            pinch_active = True #Marking that the pinch gesture has begun   
            pinch_start_time = time.time() #Recording the exact time of pinch

        pinch_duration = time.time() - pinch_start_time #Calculating how long the pinch is held

        if pinch_duration > drag_threshold: #detecting the long pinch gestures
            if not dragging:
                pyautogui.mouseDown() #Pressing and holding the left mouse
                dragging = True #Marking that dragging is active
                print("Drag Started")

            pyautogui.dragTo(screen_x, screen_y, duration = 0) #Move the mouse while holding button = dragging

        else:
            if pinch_active: #If the pinch was active previously
                pinch_duration = time.time() - pinch_start_time #Measuring how long each pinch lasted
                if pinch_duration < click_threshold: #Short pinch click 
                    pyautogui.click() #Performing the click
                    print("Click!")

                if dragging:
                    pyautogui.mouseUp() #Releasing mouse button

                    dragging = False #Dragging finished

                    print("Drag Stopped!")

            pinch_active = False #Reset pinch state


# def finger_states(hand_landmarks):
#     fingers = []
#     #Index
#     fingers.append(hand_landmarks.landmark[8])

while True: #This continuously produces the camera frames
    ret, frame = capture.read() #Reading the frames from the webcam, and ret = True if the frame is captured successfully

    if not ret: #Exit the loop if the camera frame failed
        break

    frame = cv2.flip(frame, 1) #As we want to make the system feel like a mirror, we flip the camera

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #As mediapipe requires the rgb color scheme, and openCV uses bgr scheme, we need to convert that first
    results = hands.process(rgb_frame) #This is using the hand detection model on the frame

    if results.multi_hand_landmarks: #If atleast 1 hand is detected
        for hand_landmarks in results.multi_hand_landmarks: #Iterating through the hand landmarks of the detected hand
            
            #drawing the hand skeleton for better visualization
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            ) #drawing the landmarks and the connections too

            #Extract the landmarkss of the index finger and the thumb
            index_finger = hand_landmarks.landmark[8]
            thumb = hand_landmarks.landmark[4]

            screen_x, screen_y = cursor_position(index_finger) #COnverting the finger position to the screen position
            #Also mapping the finger position to screen pixel position

            #To preent jittering 
            smooth_x = prev_x + (screen_x - prev_x) * 0.2
            smooth_y = prev_y + (screen_y - prev_y) * 0.2

            prev_x = smooth_x
            prev_y = smooth_y

            if not dragging:
                pyautogui.moveTo(screen_x, screen_y) #Moving the cursor only when we are not dragging

                distance = calculating_pinch_distance(index_finger, thumb) #Measuring the distance between the two fingers
                
                # print(distance) # qJust for if required to tune

                handling_pinch(distance, smooth_x, smooth_y) #Deciding whether to click, drag or do nothing and just move the cursor

            else: #If the cursor is draggign
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

                pinch_active = False #Reseting the pinch state

            cv2.imshow("Gesture Mouse", frame) #The webcam window

            if cv2.waitKey(1) & 0xFF == ord('q'): #Press q to quit
                break 

capture.release()
cv2.destroyAllWindows()
            








    




