# Imports
from ParkingInitializer import *
from VideoReader import *
import os

parking_init = ParkingInitializer()
parking_init.take_a_picture()
parking_init.put_rectangles()


with open("carParkPos", "rb") as f:
    print(pickle.load(f))
