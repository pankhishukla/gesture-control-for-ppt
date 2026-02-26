# 🎯 Gesture-Controlled PowerPoint Presentation

A computer vision-based gesture control system that allows you to control PowerPoint presentations and draw on slides using hand gestures detected through your webcam.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Gestures & Controls](#gestures--controls)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)

---

## ✨ Features

- **Hand Detection & Tracking**: Real-time hand detection using MediaPipe's advanced ML models
- **Gesture Recognition**: Recognize and respond to multiple hand gestures
- **Slide Navigation**: 
  - Left swipe to go to previous slide (PageUp)
  - Right swipe to go to next slide (PageDown)
- **Drawing Mode**: Use thumb and index finger pinch gesture to draw on slides
- **Mouse Control**: Move your index finger to control the mouse cursor position
- **Real-time Visualization**: See hand landmarks and connections on the webcam feed
- **Configurable Sensitivity**: Adjust thresholds for gesture detection

---

## 📦 Prerequisites

- **Python 3.11** (recommended; MediaPipe has stability issues with Python 3.12)
- **Webcam**: A working webcam for hand detection
- **Operating System**: Windows (PowerShell compatible)

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd d:\Computer Vision\Gesture\ Cntrol\ for\ PPT
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install opencv-contrib-python==4.13.0.92
pip install mediapipe==0.10.11
pip install pyautogui
pip install numpy
```

---

## 🎮 Usage

### Run the Application

```bash
python hand_detection.py
```

### Controls

Once the application is running:

| Gesture | Action |
|---------|--------|
| **Right Swipe** | Go to next slide (Page Down) |
| **Left Swipe** | Go to previous slide (Page Up) |
| **Pinch (Thumb + Index Finger)** | Start drawing on the slide |
| **Release Pinch** | Stop drawing |
| **Move Index Finger** | Control mouse cursor position |
| **Press 'Q'** | Quit the application |

---

## 🔧 Gestures & Controls

### 1. **Slide Navigation (Swipe Gesture)**

- Position your hand in the **center of the frame** (between 40-60% horizontally)
- Perform a quick swipe to the **right** → Next slide (PageDown)
- Perform a quick swipe to the **left** → Previous slide (PageUp)
- **Swipe Threshold**: 0.15 (minimum horizontal movement required)
- **Cooldown**: 1.5 seconds between swipes

### 2. **Drawing Mode (Pinch Gesture)**

- Keep your hand visible to the webcam
- Bring your **thumb and index finger close together** (distance < 0.04)
- The mouse will **activate** (mouseDown) and you can draw
- When the distance between thumb and index finger exceeds 0.12, drawing stops
- This allows for stable drawing with a "hysteresis zone"

### 3. **Mouse Movement**

- The index finger position is tracked continuously
- Your hand movements translate to mouse cursor movement
- Smoothing applied to prevent jittery movement

---

## ⚙️ Configuration

Edit the following parameters in `hand_detection.py` to fine-tune the application:

```python
# Gesture Detection Parameters
swipe_threshold = 0.15              # Minimum horizontal movement for swipe detection
cooldown = 1.5                      # Cooldown period between swipes (seconds)

# Hand Detection Zones
center_min = 0.4                    # Left boundary of center zone (0-1 normalized)
center_max = 0.6                    # Right boundary of center zone (0-1 normalized)

# Drawing Gesture Parameters
start_draw_distance = 0.04          # Distance threshold to start drawing (pinch)
stop_draw_distance = 0.12           # Distance threshold to stop drawing

# MediaPipe Hand Configuration
min_detection_confidence = 0.7      # Minimum confidence for hand detection
min_tracking_confidence = 0.7       # Minimum confidence for hand tracking
```

---

## 🐛 Troubleshooting

### Issue: "Import 'pyautogui' could not be resolved"
**Solution**: This is a VS Code interpreter issue, not a code issue. Ensure VS Code is using the correct virtual environment:
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose the interpreter from `./venv/Scripts/python.exe`

### Issue: MediaPipe Errors or Crashes
**Solution**: Downgrade to Python 3.11:
```powershell
# Uninstall current Python and install 3.11
# Then reinstall packages in the venv
pip install -r requirements.txt
```

### Issue: Hand Detection Not Working
**Causes & Solutions**:
- **Poor lighting**: Improve ambient lighting
- **Incorrect webcam**: Check that the correct camera is being used (`cv2.VideoCapture(0)`)
- **Hand too far from camera**: Get closer to the webcam
- **Hand detection confidence too low**: Review settings and ensure min_detection_confidence is appropriate

### Issue: Swipes Not Detected
**Solutions**:
- Ensure your hand is in the **center zone** (40-60% horizontally)
- Perform swipes with **faster movement**
- Adjust `swipe_threshold` to a lower value (e.g., 0.10) for more sensitivity

### Issue: Drawing is Jittery
**Solutions**:
- Improve lighting conditions
- Move closer to the webcam
- Adjust `start_draw_distance` and `stop_draw_distance` for a more stable pinch zone

---

## 📁 Project Structure

```
Gesture-Controlled-PPT/
├── hand_detection.py           # Main application with gesture detection
├── gesture-controlled-ppt.py    # FPS calculator utility
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore file
└── venv/                       # Virtual environment (after installation)
```

---

## 🔍 Technical Details

### Hand Detection Technology

- **Framework**: [MediaPipe](https://mediapipe.dev/) - Google's ML framework for building perception pipelines
- **Hand Model**: Pre-trained neural network that detects 21 hand landmarks
- **Detection Range**: Works best at 0.5-2 meters from camera
- **Accuracy**: 70% confidence threshold for reliable detection

### Key Hand Landmarks Used

- **Landmark 0**: Wrist
- **Landmark 4**: Thumb tip
- **Landmark 8**: Index finger tip
- **Landmark 12**: Middle finger tip
- **Landmark 16**: Ring finger tip
- **Landmark 20**: Pinky tip

### Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| `opencv-python` | 4.13.0.92 | Video capture and image processing |
| `mediapipe` | 0.10.11 | Hand detection and tracking |
| `pyautogui` | Latest | Keyboard and mouse control automation |
| `numpy` | 2.4.2 | Numerical computations |

---

## 🎓 Code Highlights

### Hand Detection Pipeline

```python
# Initialize hand detector
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Process each frame
results = hands.process(rgb_frame)

# Extract landmarks
for hand_landmarks in results.multi_hand_landmarks:
    wrist = hand_landmarks.landmark[0]
    thumb = hand_landmarks.landmark[4]
    index_finger = hand_landmarks.landmark[8]
```

### Gesture Recognition Example

```python
# Swipe detection
if center_min < current_x < center_max and not gesture_active:
    gesture_start_x = current_x
    gesture_active = True

if gesture_active:
    total_movement = current_x - gesture_start_x
    
    if total_movement > swipe_threshold:
        pyautogui.press("pagedown")  # Next slide
    elif total_movement < -swipe_threshold:
        pyautogui.press("pageup")    # Previous slide
```

---

## 🎯 Future Enhancements

- [ ] Multi-hand gesture support
- [ ] Voice commands integration
- [ ] Custom gesture recording and playback
- [ ] Drawing annotation tools
- [ ] Gesture undo/redo functionality
- [ ] Cross-platform support (macOS, Linux)
- [ ] Gesture logging and statistics

---

## ⚠️ Important Notes

1. **Python Version**: MediaPipe is unstable with Python 3.12. Use Python 3.11 for best results.
2. **PyAutoGUI Settings**: The code sets `FAILSAFE=False` to prevent interruptions during mouse control.
3. **Performance**: Resolution is set to 1280x720 for optimal performance and accuracy.
4. **Permissions**: Ensure your application has permission to access:
   - Webcam
   - Mouse control
   - Keyboard input

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests with improvements

---

## 💡 Tips for Best Results

1. **Lighting**: Use uniform, bright lighting without harsh shadows
2. **Background**: Use a contrasting background that's not too busy
3. **Hand Position**: Keep your hand fully visible in the camera frame
4. **Distance**: Maintain 0.5-1.5 meters from the camera
5. **Calibration**: Test gestures before presenting to ensure smooth operation
6. **Backup**: Keep a traditional presentation remote as a backup

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Author**: Computer Vision Development Teamj8jhgh5gfg48i7nhybhtgrghbg fvegvrf rf cecefvrgrgrvrgvrgvrgvrfecfcfrfexswdc3tvr