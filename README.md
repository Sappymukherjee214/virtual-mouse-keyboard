# virtual-mouse-keyboard

This project allows you to control your computer's mouse and a virtual keyboard using hand gestures detected through your webcam. It is built with Python using OpenCV, MediaPipe, and PyAutoGUI.

## Features ✨

* **Mode Switching**: Seamlessly switch between Mouse, Keyboard, and Neutral modes with a fist gesture.
* **Smoothed Mouse Control**: Jitter-free cursor movement that follows your index finger.
* **Gesture-Based Clicks**: Perform a left-click by pinching your index finger and thumb.
* **Virtual Keyboard**: Type on a screen-rendered keyboard using a dwell-to-type mechanism.

## Setup and Installation

1.  **Clone the repository or create the file structure:**
    Ensure you have the files `main.py`, `utils.py`, `gestures.md`, and `README.md` in a folder named `virtual-mouse-keyboard`.

2.  **Install dependencies:**
    Open your terminal and run the following command to install the required Python libraries.
    ```bash
    pip install opencv-python mediapipe pyautogui numpy
    ```

## How to Run

Navigate to the project directory in your terminal and run the main script:

```bash
cd path/to/virtual-mouse-keyboard
python main.py
```

A window will open showing your webcam feed. Press 'q' to quit the application at any time. Refer to `gestures.md` for a full guide on how to control the application.
