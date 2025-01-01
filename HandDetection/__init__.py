import mediapipe as mp
import math
class Hand:
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius // 2
        self.color = color

class HandDetection:
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    handsModel = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.1, min_tracking_confidence=0.1)

    @classmethod
    def __getCenters__(cls,multi_hand_landmarks,frame):
        hand_info = []
        h, w, _ = frame.shape

        for idx, hand_landmarks in enumerate(multi_hand_landmarks):
            count = 0
            sum_cx, sum_cy = 0, 0
            max_distance = 0  # Variable to store the maximum distance from the center

            # Calculate the center of the hand
            for landmark in hand_landmarks.landmark:
                cx = int(landmark.x * w)
                cy = int(landmark.y * h)
                sum_cx += cx
                sum_cy += cy
                count += 1

            center_x = sum_cx // count
            center_y = sum_cy // count

            # Calculate the maximum distance (for the radius)
            for landmark in hand_landmarks.landmark:
                cx = int(landmark.x * w)
                cy = int(landmark.y * h)
                distance = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
                if distance > max_distance:
                    max_distance = distance

            # Append the center coordinates and the radius
            hand_info.append(Hand(center_x, center_y, 30, (255, 0, 0) if idx == 0 else (0, 0, 255)))
            # hand_info.append(Hand(center_x, center_y, int(max_distance), (255, 0, 0) if idx == 0 else (0, 0, 255)))

        return hand_info

    @classmethod
    def detectHand(cls,frame):
        result = cls.handsModel.process(frame)
        if result.multi_hand_landmarks:
            hand_objects = cls.__getCenters__(result.multi_hand_landmarks,frame)
            return hand_objects
        
        return False