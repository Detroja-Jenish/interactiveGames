import cv2
import math
# from pygameRender import PyGameRender
class Camera:
    cam = cv2.VideoCapture(0)
    # cam = cv2.VideoCapture("http://192.168.144.230:4747/video")
    ret, frame = cam.read()
    height, width = frame.shape[0], frame.shape[1]
    crop = False
    x,y,w,h = 0,0,0,0
    @classmethod
    def readFrame(cls):
        cls.ret, cls.frame = Camera.cam.read()
        cls.frame = cv2.flip(cls.frame, 1)

        if cls.crop:
            cls.frame = cls.frame[cls.y:cls.y+cls.h, cls.x:cls.x+cls.w]
            cls.frame = cv2.resize(cls.frame, (cls.width, cls.height))  # Resize to (width, height)
        cls.frame = cv2.cvtColor(cls.frame, cv2.COLOR_BGR2RGB)
    
    @classmethod 
    def setCrop(cls, x,y,w,h,crop=True):
        print(x,y,w,h)
        cls.x,cls.y,cls.w,cls.h,cls.crop = x,y,w,h,crop
        # cls.height  = math.floor(cls.height * 1.5)
        # cls.width = math.floor( cls.width * 1.5)