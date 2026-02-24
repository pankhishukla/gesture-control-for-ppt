import cv2 #Used to access webcam 
import mediapipe as mp #Mediapipe is tool for hand detection and tracking
import time
import pyautogui #This library allows us to trigger by interacting with the keyboard. Bascially it creates a fake 
import math

#Without this, PyAutoGUI sometimes cancels mouse holds silently.
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands #This contains a hand detection and a tracking model

hands = mp_hands.Hands( 
    static_image_mode = False, #This is us telling the mediapipe that we are not giving you the static images, we are giving you videos, this detects my hand one time and then in future it is faster to track with smoother tracking.
    #If it was true, it would have detected from the scratch

    max_num_hands = 1, #This just tracks one hand maximum, this is for faster and creates lesser confusion

    model_complexity = 1, #Mediapipe hasa different models, and this shows the medium model used

    min_detection_confidence = 0.7, #Mediapipe should be atleast 70% sure that it is showing a hand, if the confidence is lower, it will ignore 

    min_tracking_confidence = 0.7 #This is applied after the hand is detected, tracking means following the hand across the frames

) ##Basically this only tells us where the hand is and where the hand joints are. Creates an object for hands and it will process each frame and detect hands   

mp_draw = mp.solutions.drawing_utils #This is used for and marking connections drawing the landmarks on the hand

capture = cv2.VideoCapture(0)

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #This improves the camera resolution significantly

screen_width, screen_height = pyautogui.size()
drawing = False
# previous_x = 0 #Stores the previous wrist X position

swipe_threshold = 0.15 #As a human hand shakes naturally, a hand should atleast move 0.015 points in order to consider it in the path of swiping

cooldown = 1.5 #Currently the system prints "right" or "left" many times for 1 single swipe, for this we need a cooling down period between the swipes

last_swipe_time = 0 #Storing the last position 

#These are the gesture tracking variables
gesture_start_x = None
gesture_active = False  

center_min = 0.4
center_max = 0.6

start_draw_distance = 0.04 #Creating a stability zone
stop_draw_distance = 0.12

drawing = False

while True:
    ret, frame = capture.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1) #Flipping the camera so that the swipes feels natural    

    #Open CV uses the BGR colour format but, mediapipe requires RGB colour format, hence converting
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame) #This runs the hand detection model

    #The multi_hand_landmarks contains the hand points
    if results.multi_hand_landmarks: 
        for hand_landmarks in results.multi_hand_landmarks: #looping through each of the hand detected
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks, #Drawing the landmarks
                mp_hands.HAND_CONNECTIONS #Drawing the connections between the landmarks
            )

            wrist = hand_landmarks.landmark[0] #Getting the wrist landmarks

            current_x = wrist.x #Getting the x coordinate

            # diff =  current_x - previous_x #Calculating the difference, 
            current_time = time.time()

            if center_min < current_x < center_max and gesture_active == False: #Only activating the gesture when the hand is in the center and the gesture is not active 
                gesture_start_x = current_x
                gesture_active = True

            if gesture_active and drawing == False: #Ensures that when the drawing mode means no swiping
                total_movement = current_x - gesture_start_x

                if total_movement > swipe_threshold and (current_time - last_swipe_time) > cooldown:
                    print("RIGHT") #Detecting the right swipe

                    pyautogui.press("pagedown") #Pressing the right keyq
                    last_swipe_time = current_time #Updating the last swipe time
                    gesture_active = False
                
                elif total_movement < -swipe_threshold and (current_time - last_swipe_time) > cooldown:
                    print("LEFT") #Detecting the left swipe
 
                    pyautogui.press("pageup") #Pressing the left key
                    last_swipe_time = current_time
                    gesture_active = False
                
                previous_x = current_x #Updating the previous location

            index_finger = hand_landmarks.landmark[8] #Getting the index finger point

            thumb = hand_landmarks.landmark[4] #Getting the thumb point

            #This is converting to screen coordinates
            screen_x = int(index_finger.x * screen_width)
            screen_y = int(index_finger.y * screen_height)

            # pyautogui.moveTo(screen_x, screen_y, duration = 0.01) #This is to move the mouse to the finger position, duration adds micro smoothening
            screen_x = max(1, min(screen_x, screen_width - 1))
            screen_y = max(1, min(screen_y, screen_height - 1))

            pyautogui.moveTo(screen_x, screen_y)

            
            distance = math.hypot( 
                index_finger.x - thumb.x,
                index_finger.y - thumb.y
            ) #This calculating the distance between the index finger and the thumb

            # if distance < start_draw_distance: #If the distance between the fingers is too close, it will start drawing
            #     if drawing == False:
            #         pyautogui.mouseDown()
            #         drawing = True
            #         print("Started drawing!!")

            # elif distance > stop_draw_distance: #If the distance between the fingers is far enough, it will stop drawing
            #     if drawing == True:
            #         pyautogui.mouseUp()
            #         drawing = False
            #         print("Stopped Drawing!!")

            if distance < start_draw_distance:
                if drawing == False:
                    print("MOUSEDOWN TRIGGERED")
                    pyautogui.mouseDown()
                    drawing = True

            elif distance > stop_draw_distance:
                if drawing == True:
                    print("MOUSEUP TRIGGERED")
                    pyautogui.mouseUp()
                    drawing = False
    
    else:  
        gesture_active = False #Reseting the gesture when the hand disappears, when it is not in the frame

        if drawing:
            pyautogui.mouseUp()
            drawing = False #Releasing the mouse when the hand disappears from the frame

    cv2.imshow("Gesture Control PPT", frame) #Basically a window for showing the detecqted hands

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()