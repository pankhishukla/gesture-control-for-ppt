import cv2 #Used to access webcam 
import mediapipe as mp #Mediapipe is tool for hand detection and tracking

mp_hands = mp.solutions.hands #This contains a hand detection and a tracking model
hands = mp_hands.Hands() #Creates an object for hands and it will process each frame and detect hands

mp_draw = mp.solutions.drawing_utils #This is used for and marking connections drawing the landmarks on the hand

capture = cv2.VideoCapture(0)

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

    cv2.imshow("Hand Detection", frame) #Basically a window for showing the detected hands

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

