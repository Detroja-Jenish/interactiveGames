import cv2
class Camera:
    # cam = cv2.VideoCapture(0)
    # http://192.168.0.101:4747/video
    cam = cv2.VideoCapture("http://192.168.144.230:4747/video")
    ret, frame = cam.read()
    height, width, _ = frame.shape

    @classmethod
    def readFrame(cls):
        cls.ret, cls.frame = Camera.cam.read()
        cls.frame = cv2.flip(cls.frame, 1)
        cls.frame = cv2.cvtColor(cls.frame, cv2.COLOR_BGR2RGB)