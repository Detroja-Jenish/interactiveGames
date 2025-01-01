import cv2
from gameGlobals import GameGlobals
import json
# from pygameRender import PyGameRender
class Camera:
    cam = cv2.VideoCapture(0)
    # cam = cv2.VideoCapture("http://192.168.144.230:4747/video")
    ret, frame = cam.read()
    height, width = GameGlobals.screen_height,GameGlobals.screen_width 
    x,y,w,h = 0,0,0,0
    video_writer = cv2.VideoWriter("output.mp4",cv2.VideoWriter_fourcc(*'mp4v') ,30,(GameGlobals.screen_width ,GameGlobals.screen_height))
    @classmethod
    def readFrame(cls):
        cls.ret, cls.frame = Camera.cam.read()
        cls.frame = cv2.flip(cls.frame, 1)
        cls.frame = cv2.resize(cls.frame, (cls.width, cls.height))
        if GameGlobals.isCameraCallibered:
            cls.video_writer.write(cls.frame)
            cls.frame = cls.frame[cls.y:cls.y+cls.h, cls.x:cls.x+cls.w]
            cls.frame = cv2.resize(cls.frame, (cls.width, cls.height))  # Resize to (width, height)
        cls.frame = cv2.cvtColor(cls.frame, cv2.COLOR_BGR2RGB)
    
    @classmethod 
    def setCrop(cls, x,y,w,h):
        cls.x,cls.y,cls.w,cls.h = x,y,w,h
        