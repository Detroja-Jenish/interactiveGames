import cv2
from gameGlobals import GameGlobals
# from pygameRender import PyGameRender
class Camera:
    cam = cv2.VideoCapture(0)
    # cam = cv2.VideoCapture("http://192.168.144.230:4747/video")
    ret, frame = cam.read()
    # height, width = frame.shape[0], frame.shape[1]
    height, width = GameGlobals.screen_height,GameGlobals.screen_width 
    crop = False
    x,y,w,h = 0,0,0,0
    video_writer = cv2.VideoWriter("output.mp4",cv2.VideoWriter_fourcc(*'mp4v') ,30,(GameGlobals.screen_width ,GameGlobals.screen_height))
    @classmethod
    def readFrame(cls):
        cls.ret, cls.frame = Camera.cam.read()
        cls.frame = cv2.flip(cls.frame, 1)
        cls.frame = cv2.resize(cls.frame, (cls.width, cls.height))
        if cls.crop:
            cls.video_writer.write(cls.frame)
            cls.frame = cls.frame[cls.y:cls.y+cls.h, cls.x:cls.x+cls.w]
            cls.frame = cv2.resize(cls.frame, (cls.width, cls.height))  # Resize to (width, height)
        cls.frame = cv2.cvtColor(cls.frame, cv2.COLOR_BGR2RGB)
    
    @classmethod 
    def setCrop(cls, x,y,w,h,crop=True):
        print(x,y,w,h)
        cls.x,cls.y,cls.w,cls.h,cls.crop = x,y,w,h,crop
        # cls.height  = math.floor(cls.height * 1.5)
        # cls.width = math.floor( cls.width * 1.5)