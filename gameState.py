from ball import Ball
import random 
import mediapipe as mp
from gameGlobals import GameGlobals

class GameState:
    ball = Ball(x=random.randint(50, GameGlobals.screen_width-50), y=random.randint(50, GameGlobals.screen_height-50), radius=40, color=(0, 0, 0), speed_x=20, speed_y=20)
    left_score = 0 
    right_score = 0
    running = True
    state = 'start' # 'start' | 'play' | 'crop'
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    handsModel = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.1, min_tracking_confidence=0.1)
    
