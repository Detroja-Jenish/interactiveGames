import math
from hand import Hand
# Function to get centers and radius of the bounding circles for hands
def get_centers(multi_hand_landmarks, frame):
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
        hand_info.append(Hand(center_x, center_y, int(max_distance), (255, 0, 0) if idx == 0 else (0, 0, 255)))

    return hand_info
