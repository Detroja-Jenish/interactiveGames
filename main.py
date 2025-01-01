import cv2
from ping_pong_game import game_loop
import pygame

from yolo_detector import YOLODetector

# Load YOLO Model
detector = YOLODetector("yolo_weights/best.pt")

# Capture from webcam
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

def main():
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO: Get hand coordinates
        hand_coords = detector.get_hand_coordinates(frame)
        if hand_coords:
            hand_x, hand_y = hand_coords
        else:
            hand_x, hand_y = 0, 0  # Default paddle position if hand not detected

        # Convert OpenCV frame (BGR to RGB)
        cv2.imshow('Webcam', frame)

        # Pygame: Update game with detected hand_y position
        game_loop(hand_y)

        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()
