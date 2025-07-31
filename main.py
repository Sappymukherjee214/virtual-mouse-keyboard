import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import utils # Import our utility functions

class VirtualController:
    """
    The main class to control the mouse and keyboard using hand gestures.
    """
    def __init__(self, smoothing=7, click_thresh=0.045, dwell_time=1.0):
        # --- System and Screen ---
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()

        # --- Camera ---
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")
        self.cam_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cam_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # --- Hand Tracking ---
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.hand_landmarks = None

        # --- Control Modes & State ---
        self.modes = ['NEUTRAL', 'MOUSE', 'KEYBOARD']
        self.current_mode = 'NEUTRAL'
        self.mode_switch_time = 0

        # --- Mouse Control ---
        self.plocx, self.plocy = 0, 0
        self.smoothing = smoothing
        self.click_threshold = click_thresh

        # --- Keyboard Control ---
        self.key_boxes = utils.create_keyboard_layout()
        self.dwell_time = dwell_time
        self.hover_start_time = None
        self.hovered_key = None

    def _process_gestures(self):
        """Identifies and acts on hand gestures based on the current mode."""
        if not self.hand_landmarks:
            return

        landmarks = self.hand_landmarks.landmark
        
        # Mode Switching Gesture (Fist)
        is_fist = (utils.calculate_distance(landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP], landmarks[self.mp_hands.HandLandmark.WRIST]) <
                   utils.calculate_distance(landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP], landmarks[self.mp_hands.HandLandmark.WRIST]))

        if is_fist and (time.time() - self.mode_switch_time > 1.5): # Debounce switch
            current_index = self.modes.index(self.current_mode)
            self.current_mode = self.modes[(current_index + 1) % len(self.modes)]
            print(f"Mode switched to: {self.current_mode}")
            self.mode_switch_time = time.time()

        # Mode-specific logic
        if self.current_mode == 'MOUSE':
            self._handle_mouse_control(landmarks)
        elif self.current_mode == 'KEYBOARD':
            self._handle_keyboard_control(landmarks)

    def _handle_mouse_control(self, landmarks):
        """Manages mouse actions like movement and clicking."""
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = landmarks[self.mp_hands.HandLandmark.THUMB_TIP]

        # Cursor Movement
        x = np.interp(index_tip.x, (0.1, 0.9), (0, self.screen_width))
        y = np.interp(index_tip.y, (0.1, 0.9), (0, self.screen_height))
        clocx = self.plocx + (x - self.plocx) / self.smoothing
        clocy = self.plocy + (y - self.plocy) / self.smoothing
        pyautogui.moveTo(clocx, clocy)
        self.plocx, self.plocy = clocx, clocy

        # Left Click (Index and Thumb pinch)
        if utils.calculate_distance(index_tip, thumb_tip) < self.click_threshold:
            pyautogui.click()
            time.sleep(0.3) # Debounce click

    def _handle_keyboard_control(self, landmarks):
        """Manages virtual keyboard interactions with dwell-to-type."""
        index_tip = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        tip_x_pixel = int(index_tip.x * self.cam_width)
        tip_y_pixel = int(index_tip.y * self.cam_height)
        
        currently_hovering_key = None
        for key in self.key_boxes:
            x1, y1, x2, y2 = key['rect']
            if x1 < tip_x_pixel < x2 and y1 < tip_y_pixel < y2:
                currently_hovering_key = key
                break
        
        if currently_hovering_key:
            if self.hovered_key and self.hovered_key['char'] == currently_hovering_key['char']:
                # Check for dwell time
                if time.time() - self.hover_start_time > self.dwell_time:
                    pyautogui.press(currently_hovering_key['char'])
                    print(f"Typed: {currently_hovering_key['char']}")
                    self.hover_start_time = time.time() # Reset timer
            else:
                # New key is being hovered
                self.hovered_key = currently_hovering_key
                self.hover_start_time = time.time()
        else:
            self.hovered_key = None
            self.hover_start_time = None

    def run(self):
        """Main application loop."""
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success: continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            self.hand_landmarks = results.multi_hand_landmarks[0] if results.multi_hand_landmarks else None
            
            if self.hand_landmarks:
                self.mp_draw.draw_landmarks(frame, self.hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                self._process_gestures()

            hovered_char = self.hovered_key['char'] if self.hovered_key else None
            utils.draw_elements(frame, self.current_mode, self.key_boxes, self.cam_height, hovered_char)
            
            cv2.imshow("Virtual Controller", frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    controller = VirtualController()
    controller.run()