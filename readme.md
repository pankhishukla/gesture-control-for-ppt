# Gesture-Controlled PPT (Hand Gesture Mouse)

Control your cursor with hand gestures using a webcam, MediaPipe, OpenCV, and PyAutoGUI.

This project tracks one hand in real-time and maps the index finger position to mouse movement. It also detects an index-thumb pinch to perform click and drag interactions.

## Features

### Implemented
- Real-time hand tracking using MediaPipe
- Cursor movement using index fingertip
- Left click using quick index-thumb pinch
- Drag and hold using longer index-thumb pinch
- Live hand landmark visualization

### In Progress / Planned
- Right click gesture
- Scroll gesture
- Slide navigation gestures (left/right swipe)
- Presentation-specific mode and gesture tuning

## Project Structure

- `hand_detection.py`: Main gesture-to-mouse controller
- `gesture-controlled-ppt.py`: Webcam + FPS test utility
- `requirements.txt`: Python dependencies
- `readme.md`: Project documentation

## Tech Stack

- Python 3.9+
- OpenCV
- MediaPipe
- PyAutoGUI

## Requirements

1. A working webcam
2. Windows/macOS/Linux desktop environment (PyAutoGUI requires GUI access)
3. Python installed and available in terminal

## Installation

### 1) Clone the repository

```bash
git clone <your-repo-url>
cd "Gesture Cntrol for PPT"
```

### 2) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

## Run

Run the main controller:

```bash
python hand_detection.py
```

Press `q` in the OpenCV window to quit.

Optional camera/FPS test:

```bash
python gesture-controlled-ppt.py
```

## Gesture Controls (Current)

| Gesture                     | Action         | Status      |
| Index finger move           | Move cursor    | Implemented |
| Index + thumb pinch (quick) | Left click     | Implemented |
| Index + thumb pinch (hold)  | Drag           | Implemented |
| Middle + thumb pinch        | Right click    | Planned     |
| Index + middle fingers up   | Scroll         | Planned     |
| Palm swipe right            | Next slide     | Planned     |
| Palm swipe left             | Previous slide | Planned     |

## How It Works

1. Webcam frame is captured and mirrored.
2. Frame is converted to RGB and passed to MediaPipe Hands.
3. Index fingertip coordinates are mapped to screen coordinates.
4. Thumb-index distance is measured to detect pinch events.
5. Pinch duration determines click vs drag.

## Tuning Parameters

In `hand_detection.py`, adjust these values for your camera and hand distance:

- `pinch_threshold`: Distance threshold to detect pinch
- `click_threshold`: Max pinch time to register click
- `drag_threshold`: Pinch hold time to start drag

## Troubleshooting

### Camera not opening
- Ensure no other app is using the webcam.
- Try changing camera index in `cv2.VideoCapture(0)` to `1` or `2`. This allows the webcam to access other cameras than the default one.

### Cursor is jittery
- Improve room lighting.
- Keep hand in frame and reduce fast motion.
- Increase smoothing factor logic in `hand_detection.py`.

### Click/drag not reliable
- Recalibrate pinch thresholds.
- Keep hand at a consistent distance from camera.

### PyAutoGUI issues
- Some systems block automated mouse control due to permissions.
- On Linux/macOS, ensure accessibility/input permissions are granted.

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

## License

Add your preferred license here (for example, MIT).

