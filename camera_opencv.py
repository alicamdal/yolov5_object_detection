import os
import cv2
from camera_generator import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    stream = """
        nvarguscamerasrc !
        video/x-raw(memory:NVMM), width=(int)640, height=(int)640, framerate=(fraction)60/1 ! 
        nvvidconv flip-method=0 ! 
        video/x-raw, width=(int)640, height=(int)640, format=(string)BGRx ! 
        videoconvert ! 
        video/x-raw, format=(string)BGR ! appsink
        """

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        #camera = cv2.VideoCapture(Camera.stream, cv2.CAP_GSTREAMER)
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        while True:
            _, img = camera.read()
            yield img
