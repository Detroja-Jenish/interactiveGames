import mediapipe as mp
import cv2
import math

def get_centers(multi_hand_landmarks,frame):
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
        hand_info.append((idx,(center_x, center_y) , int(max_distance)))

    return hand_info

          
mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.1,min_tracking_confidence=0.1).process(frame)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        centeres = get_centers(results.multi_hand_landmarks,frame)
        for idx,coordinates,radius in centeres:
            cx,cy=coordinates
            cv2.circle(frame, (coordinates[0], coordinates[1]), radius, (255,0,0,0.3))

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()