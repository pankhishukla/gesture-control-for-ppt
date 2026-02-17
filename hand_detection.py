import cv2 #Used to access webcam 
import mediapipe as mp #Mediapipe is tool for hand detection and tracking

mp_hands = mp.solutions.hands #This contains a hand detection and a tracking model
hands = mp_hands.Hands() #Creates an object for hands and it will process each frame and detect hands

mp_draw = mp.solutions.drawing_utils #This is used for and marking connections drawing the landmarks on the hand

capture = cv2.VideoCapture(0)

previous_x = 0 #Stores the previous wrist X position

threshold = 0.08 #As a human hand shakes naturally, a hand should atleast move 0.08 points in order to consider it in the path of swiping

while True:
    ret, frame = capture.read()

    if not ret:
        break

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

            diff =  current_x - previous_x #Calculating the difference, 

            if diff > threshold:
                print("RIGHT") #Detecting the right swipe
            
            elif diff < -threshold:
                print("LEFT") #Detecting the left swipe

            
            previous_x = current_x #Updating the previous location
        
    cv2.imshow("Swipe Detection", frame) #Basically a window for showing the detected hands

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

