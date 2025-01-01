import mediapipe as mp
import cv2

def get_centers(multi_hand_landmarks,frame):
    centeres = []
    h, w, c = frame.shape
    for idx, hand_landmarks in enumerate(multi_hand_landmarks):
        count = 0
        sum_cx,sum_cy=0,0
        for landmark in hand_landmarks.landmark:
            sum_cx += int(landmark.x * w)
            sum_cy += int(landmark.y * h)
            # cx, cy = int(landmark.x * w), int(landmark.y * h)
            count += 1
        centeres.append((idx,(sum_cx//count,sum_cy//count)))
    return centeres

          
mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
img = cv2.imread("assets/rock_climbing_3.jpg")
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
results=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.1,min_tracking_confidence=0.1).process(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

if results.multi_hand_landmarks:
    centeres = get_centers(results.multi_hand_landmarks,img)
    for idx,coordinates in centeres:
        cx,cy=coordinates
        cv2.circle(img, (coordinates[0], coordinates[1]), 40, (255,0,0,0.3))

cv2.imshow("testing",img)
cv2.waitKey(0)

cv2.destroyAllWindows()

cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.1,min_tracking_confidence=0.1).process(frame)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        centeres = get_centers(results.multi_hand_landmarks,frame)
        for idx,coordinates in centeres:
            cx,cy=coordinates
            cv2.circle(frame, (coordinates[0], coordinates[1]), 40, (255,0,0,0.3))

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()