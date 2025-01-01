from ball import Ball
import random 
from camera import Camera
import mediapipe as mp

class GameState:
    ball = Ball(x=random.randint(50, Camera.width-50), y=random.randint(50, Camera.height-50), radius=15, color=(0, 255, 0), speed_x=5, speed_y=5)
    left_score = 0 
    right_score = 0
    running = True
    state = 'start' # 'start' | 'play' | 'crop'
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    handsModel = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.1, min_tracking_confidence=0.1)
    
