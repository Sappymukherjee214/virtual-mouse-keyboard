import cv2
import math

# --- Keyboard Configuration ---
KEYBOARD_LAYOUT = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

def create_keyboard_layout():
    """Creates bounding boxes for each key on the virtual keyboard."""
    key_boxes = []
    key_width, key_height = 60, 60
    key_margin = 10
    start_x, start_y = 50, 50
    
    for i, row in enumerate(KEYBOARD_LAYOUT):
        for j, key_char in enumerate(row):
            x = start_x + j * (key_width + key_margin)
            y = start_y + i * (key_height + key_margin)
            key_boxes.append({'rect': (x, y, x + key_width, y + key_height), 'char': key_char})
    return key_boxes

def calculate_distance(p1, p2):
    """Calculates Euclidean distance between two landmark points."""
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def draw_elements(frame, mode, key_boxes, cam_height, hovered_key_char=None):
    """Draws UI elements like the keyboard and mode indicator."""
    # Draw mode indicator
    cv2.putText(frame, f"Mode: {mode}", (10, cam_height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    # Draw keyboard if in KEYBOARD mode
    if mode == 'KEYBOARD':
        for key in key_boxes:
            x1, y1, x2, y2 = key['rect']
            char = key['char']
            
            # Highlight hovered key
            if char == hovered_key_char:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            
            cv2.putText(frame, char, (x1 + 20, y1 + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)