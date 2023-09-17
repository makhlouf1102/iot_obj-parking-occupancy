import cv2 as cv
import cvzone
import pickle
import numpy as np
# from rpi_lcd import LCD
from threading import Thread

class VideoReader:
    
    def __init__(self, camera_port=0):
        self.stream = cv.VideoCapture(camera_port)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
    
    def stop(self):
        self.stopped = True