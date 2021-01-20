import cv2
import numpy as np
import math
import pandas as pd

'''
this isn't anything important
'''


# VIDEO = cv2.VideoCapture("test-tube.mp4")
# WIDTH = VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH)
# WIDTH = (int)(WIDTH)
# HEIGHT = VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT) 
# HEIGHT = (int)(HEIGHT)
# MIDDLE = (int)(HEIGHT/2)

#average of pixels
def brightness(x=int(512/2), y=int(512/2), img=None):
    if img is None:
        print("No image found.")
        return 0
    
    brightness = (sum(img[y, x, :]))/3 #average of BGR values = brightness
    return int(brightness)

#https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
def getBrightness(x, y, img):
    blueChannnel = 0.299 * (math.pow(img[x, y, 0], 2))
    greenChannel = 0.587 * (math.pow(img[x, y, 1], 2))
    redChannel = 0.114 * (math.pow(img[y, x, 2], 2))
    brightness = blueChannnel+greenChannel+redChannel

    return brightness


table = []
for x in range(256):
    value1 = x%10
    value2 = x%20

    table.append([value1, value2, x])

for x in range(len(table)):
    print(table[x])
    print("\n")
