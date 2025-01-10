from ultralytics import YOLO
import cv2
import math

class GetKeypoint:
    NOSE           = 0
    LEFT_EYE       = 1
    RIGHT_EYE      = 2
    LEFT_EAR       = 3
    RIGHT_EAR      = 4
    LEFT_SHOULDER  = 5
    RIGHT_SHOULDER = 6
    LEFT_ELBOW     = 7
    RIGHT_ELBOW    = 8
    LEFT_WRIST     = 9
    RIGHT_WRIST    = 10
    LEFT_HIP       = 11
    RIGHT_HIP      = 12
    LEFT_KNEE      = 13
    RIGHT_KNEE     = 14
    LEFT_ANKLE     = 15
    RIGHT_ANKLE    = 16
class Hand:
    def __init__(self, center_x, center_y,point1,point2,radius=70, color=(255,0,0)):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius // 2
        self.color = color
        self.point1 = point1
        self.point2 = point2
class Leg(Hand):
    pass
class Nose(Hand):
    pass

class Person:
    def __init__(self,rightHand=None, leftHand=None, rightLeg=None, leftLeg=None, nose=None):
        self.rightHand = rightHand
        self.leftHand = leftHand
        self.leftLeg = leftLeg
        self.rightLeg = rightLeg
        self.nose = nose
    def getNotNoneValues(self,takeRightHand=True, takeLeftHand=True, takeRightLeg=True, takeLeftLeg=True, takeNose=True):
        arr = []
        if self.leftHand and takeLeftHand:arr.append(self.leftHand)
        if self.rightHand and takeRightHand: arr.append(self.rightHand)
        if self.leftLeg and takeLeftLeg: arr.append(self.leftLeg)
        if self.rightLeg and takeRightLeg: arr.append(self.rightLeg)
        if self.nose and takeNose: arr.append(self.nose)
        return arr

class PoseEstimater:
    model = YOLO("yolo11n-pose.pt")
    @classmethod
    def extendLine(cls,pt1,pt2,distance=10):
        x1,y1 = tuple(pt1.astype(int))
        x2,y2 = tuple(pt2.astype(int))
        if x1==0 and y1==0 or x2==0 and y2==0:
            raise "error by extending line" 
        dx = x2 - x1
        dy = y2 - y1
        n=distance
        m = int(math.sqrt(dx**2 + dy**2)) + distance
        gcd_m_n = math.gcd(m,n)
        m = m // gcd_m_n
        n = n // gcd_m_n
        x = (m*x2 - n*x1)//(m-n)
        y = (m*y2 - n*y1)//(m-n)

        return {"x": x, "y":y}
    
    @classmethod
    def getPersonsKeypoints(cls,keypoints):
        person = Person()
        try:
            leftElbow = keypoints[GetKeypoint.LEFT_ELBOW]
            rightElbow = keypoints[GetKeypoint.RIGHT_ELBOW]
            leftWrist = keypoints[GetKeypoint.LEFT_WRIST]
            rightWrist = keypoints[GetKeypoint.RIGHT_WRIST]
            leftKnee = keypoints[GetKeypoint.LEFT_KNEE]
            leftAnkle = keypoints[GetKeypoint.LEFT_ANKLE]
            rightKnee = keypoints[GetKeypoint.RIGHT_KNEE]
            rightAnkle = keypoints[GetKeypoint.RIGHT_ANKLE]
            leftEar = keypoints[GetKeypoint.LEFT_EAR]
            rightEar = keypoints[GetKeypoint.RIGHT_EAR]
            nose = keypoints[GetKeypoint.NOSE]
        except Exception:
            pass

        try:
            hand1_cordinates = cls.extendLine(leftElbow, leftWrist,100)
            if hand1_cordinates["x"] != 0 and hand1_cordinates["y"] != 0:
                person.leftHand = Hand(hand1_cordinates["x"],hand1_cordinates["y"],  leftElbow, leftWrist)
        except Exception:
            pass
        try:
            hand2_cordinates = cls.extendLine(rightElbow, rightWrist,100)
            if hand2_cordinates["x"] != 0 and hand2_cordinates["y"] != 0:
                person.rightHand = Hand(hand2_cordinates["x"],hand2_cordinates["y"],  rightElbow, rightWrist)
        except Exception:
            pass

        try:
            leg1_cordinates = cls.extendLine(leftKnee, leftAnkle,50)
            if leg1_cordinates["x"] != 0 and leg1_cordinates["y"] != 0:
                person.leftLeg=Hand(leg1_cordinates["x"],leg1_cordinates["y"],  leftKnee, leftAnkle)
        except Exception:
            pass

        try:
            leg2_cordinates = cls.extendLine(rightKnee, rightAnkle,50)
            if leg2_cordinates["x"] != 0 and leg2_cordinates["y"] != 0:
                person.rightLeg = Hand(leg2_cordinates["x"],leg2_cordinates["y"],  rightKnee, rightAnkle)
        except Exception:
            pass
        try:
            if nose[0] != 0 and nose[1] != 0:
                person.nose = Hand(int(nose[0]),int(nose[1]), leftEar,rightEar)
        except Exception as e:
            pass


        return person
    
    @classmethod
    def detectPersons(cls,frame):
        persons = []
        results = cls.model(frame)
        for result in results:
            for keypoints in result.keypoints.xy.cpu().numpy():
                persons.append(cls.getPersonsKeypoints(keypoints))
        
        return persons if len(persons) > 0 else None
    
    @classmethod
    def draw_poses(cls, frame):
        results = cls.model(frame)
        for result in results:
            for keypoints in result.keypoints.xy.cpu().numpy():
                for pt in keypoints:
                    cv2.circle(frame,(tuple(pt.astype(int))),5,(255,255,0),0)
        return frame
