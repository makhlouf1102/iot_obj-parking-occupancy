from aliot.aliot_obj import AliotObj
from parking_state import ParkingState

from ParkingInitializer import * 
from VideoReader import *
import cv2 as cv
import cvzone
import pickle
import numpy as np
# from rpi_lcd import LCD
import time
import os
import socket

parking = AliotObj("parking")

# the state of your object should be defined in this class
parking_state = ParkingState()


# write your listeners and receivers here
with open("carParkPos", "rb") as f:
    posList = pickle.load(f)

# dilate the image
def preProcessing(img):
    """
    Function that dilates the image
    """
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 1)
    imgTreshHold = cv.adaptiveThreshold(
        imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv.medianBlur(imgTreshHold, 3)
    kernel = np.ones((3, 3), np.int8)
    imgDilate = cv.dilate(imgMedian, kernel, iterations=1)
    return imgDilate

def checkParkinSpaces(img, imgProcess, posList, height=70, width=60, id=0):
    """
    Function the parking space and shows if there is some one or not
    """
    camera = [0, 0,]
    # print(posList)
    parking_places = [0]*len(posList)
    for i in range(len(posList)):
        pos = posList[i]
        x = pos[0]
        y = pos[1]

        imgCropped = imgProcess[
            y - (height // 2) : y + (height // 2), x - (width // 2) : x + (width // 2)
        ]
        count = cv.countNonZero(imgCropped)
        cvzone.putTextRect(
            img,
            str(count),
            (x - (width // 2), y + (height // 2) - 10),
            scale=1,
            thickness=1,
            offset=0,
        )
        print(count)
        if count > 700:
            color = (0, 0, 255)
            cv.rectangle(
                img,
                (x - (width // 2), y - (height // 2)),
                (x + (width // 2), y + (height // 2)),
                color,
                2,
            )
            parking_places[i] = 2
            print("true")
        else:
            color = (0, 255, 0)
            cv.rectangle(
                img,
                (x - (width // 2), y - (height // 2)),
                (x + (width // 2), y + (height // 2)),
                color,
                2,
            )
            print("false")
            parking_places[i] = 0
        result = ""
        # for element in parking_places:
        #     result+= element+";"
        # print(parking_places)
        result = "parking_camera:"+result 
        print(parking_places)
        parking.update_doc({
            '/doc/parking': parking_places
        })
        # send(result)






def start():
    height = 70
    width = 60

    # lcd = LCD()
    time.sleep(10)
    videoReader = VideoReader(0)
    video_getter = videoReader.start()
    cap = videoReader.stream
    print("Salu")

    while True:
        if (cv.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break
        frame = video_getter.frame
        imgDilate = preProcessing(frame)
        
        if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)

        checkParkinSpaces(
            frame, imgDilate, posList, height, width
        )
        
        for pos in posList:
            x = pos[0]
            y = pos[1]
            cv.rectangle(
                frame,
                (x - (width // 2), y - (height // 2)),
                (x + (width // 2), y + (height // 2)),
                (255, 0, 255),
                2,
            )
            # cv.rectangle(
            #     imgDilate,
            #     (x - (width // 2), y - (height // 2)),
            #     (x + (width // 2), y + (height // 2)),
            #     (255, 0, 255),
            #     2,
            # )
        cv.imshow("Video", frame)


def end():
    # write the code you want to execute once your object is disconnected from the server
    pass


parking.on_start(callback=start)
parking.on_end(callback=end)
parking.run()  # connects your object to the sever
