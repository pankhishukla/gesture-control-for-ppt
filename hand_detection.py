import cv2 #Used to access webcam 
import mediapipe as mp #Mediapipe is tool for hand detection and tracking
import time
import pyautogui #This library allows us to trigger by interacting with the keyboard. Bascially it creates a fake keyboard

mp_hands = mp.solutions.hands #This contains a hand detection and a tracking model
hands = mp_hands.Hands() #Creates an object for hands and it will process each frame and detect hands   

mp_draw = mp.solutions.drawing_utils #This is used for and marking connections drawing the landmarks on the hand

capture = cv2.VideoCapture(0)

# previous_x = 0 #Stores the previous wrist X position

swipe_threshold = 0.20 #As a human hand shakes naturally, a hand should atleast move 0.08 points in order to consider it in the path of swiping

cooldown = 1.5 #Currently the system prints "right" or "left" many times for 1 single swipe, for this we need a cooling down period between the swipes

last_swipe_time = 0 #Storing the last position 

#These are the gesture tracking variables
gesture_start_x = None
gesture_active = False  

center_min = 0.4
center_max = 0.6

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

            if gesture_active:
                total_movement = current_x - gesture_start_x

                if total_movement > swipe_threshold and (current_time - last_swipe_time) > cooldown:
                    print("RIGHT") #Detecting the right swipe

                    pyautogui.press("right") #Pressing the right keyq
                    last_swipe_time = current_time #Updating the last swipe time
                    gesture_active = False
                
                elif total_movement < -swipe_threshold and (current_time - last_swipe_time) > cooldown:
                    print("LEFT") #Detecting the left swipe

                    pyautogui.press("left") #Pressing the left key
                    last_swipe_time = current_time
                    gesture_active = False
                
                previous_x = current_x #Updating the previous location
    
    else:  
        gesture_active = False #Reseting the gesture when the hand disappears, when it is not in the frame

        
    cv2.imshow("Gesture Control PPT", frame) #Basically a window for showing the detecqted hands

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

