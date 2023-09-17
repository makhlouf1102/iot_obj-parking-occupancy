# imports
import cv2 as cv
import numpy as np
import pickle

class  ParkingInitializer :
    """
    A class to take a picture and let the user to draw rectangles into the image.
    
    ...
    
    Attributes
    ----------
    camera_port : int
        the port of your camera, it is 0 by default
        
    Methods
    -------
    take_a_picture():
        function to take a picture
        
    mouseClick():
        function that let the user to take put on rectangle by getting the x and y and the mouse event
        
    put_rectangles():
        shows the image to the user and let him draw rectangles on the image.
    
    """
    def __init__(self, camera_port: int = 0, height: int = 70, width: int = 60):
        self.cam = cv.VideoCapture(camera_port)
        self.__image = 0
        self.height = height
        self.width = width
        self.__posList = []
    
    def take_a_picture(self):
        result, self.__image = self.cam.read()
        if result:
            cv.imwrite("Parking.png", self.__image)
            
            cv.waitKey(0)
            print("Image saved")
        else:
            print("No Image detected.")
    
    def mouseClick(self, events, x, y, flags, params):
        if events == cv.EVENT_LBUTTONDOWN:
            self.__posList.append((x, y))

        # if events == cv.EVENT_RBUTTONDOWN:
        #     for i, pos in enumerate(self.__posList):
        #         x1, y1 = pos
        #         if (
        #             x1 - (self.width // 2) < x < x1 + self.width
        #             and 
        #             y1 - (self.height // 2) < y < y1 + self.height
        #         ):
        #             self.__posList.pop(i)
        with open("carParkPos", "wb") as f:
            pickle.dump(self.__posList, f)
    
        
    def put_rectangles(self):
        # try:
        #     with open("carParkPos", "rb") as f:
        #         self.__posList = pickle.load(f)
        # except:
        #     self.__posList = []
        
        self.__posList = []
        while True:
            for pos in self.__posList:
                x = pos[0]
                y = pos[1]
                cv.rectangle(
                    self.__image,
                    (x - (self.width // 2), y - (self.height // 2)),
                    (x + (self.width // 2), y + (self.height // 2)),
                    (255, 0, 255),
                    2,
                )
            
            cv.imshow("image", self.__image)
            
            cv.setMouseCallback("image", self.mouseClick)
            
            if cv.waitKey(1) & 0xFF == ord("q"):
                cv.destroyAllWindows()
                break
    
    def get_pos_list(self):
        return self.__posList