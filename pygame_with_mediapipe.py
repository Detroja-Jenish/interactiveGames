import mediapipe as mp
import cv2
import math
import pygame

# Initialize Pygame
pygame.init()
cam = cv2.VideoCapture(0)
ret, frame = cam.read()
# Set the dimensions of the Pygame window (same as the camera resolution)
height,width,_ = frame.shape
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hand Bounding Circle")

# Function to get centers and radius of the bounding circles for hands
def get_centers(multi_hand_landmarks, frame):
    hand_info = []
    h, w, c = frame.shape

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
            # Calculate the distance between the current landmark and the center
            distance = math.sqrt((cx - center_x)**2 + (cy - center_y)**2)
            if distance > max_distance:
                max_distance = distance

        # Append the center coordinates and the radius
        hand_info.append((idx, (center_x, center_y), int(max_distance)))

    return hand_info

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.1, min_tracking_confidence=0.1)

running = True
while running:
    ret, frame = cam.read()
    if not ret:
        break
    
    # Convert the frame to RGB for processing
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    
    # Process results and draw the hand bounding circles
    if results.multi_hand_landmarks:
        centers = get_centers(results.multi_hand_landmarks, frame)

        # Fill the Pygame screen with black color
        screen.fill((0, 0, 0))

        # Draw circles for each hand
        for idx, (cx, cy), radius in centers:
            color = (255, 0, 0) if idx == 0 else (0, 0, 255)  # Red for the first hand, blue for the second
            pygame.draw.circle(screen, color, (cx, cy), radius, 2)

        # Update the Pygame display
        pygame.display.flip()

    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release the camera and quit Pygame
cam.release()
pygame.quit()
