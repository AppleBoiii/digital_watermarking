import cv2
import numpy as np
import math

# VIDEO_NAME = input("Gimme video name + file extension: ")
VIDEO_NAME = "test-tube.mp4"
#ENCODED_NAME = input("give desired name of encoded video (rn only .avi extensions work: ")

#gets width, height, and middle-height of the image
VIDEO = cv2.VideoCapture(VIDEO_NAME)
WIDTH = VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH)
WIDTH = (int)(WIDTH)
HEIGHT = VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT) 
HEIGHT = (int)(HEIGHT)
MIDDLE = (int)(HEIGHT/2)

def getSquare():
    while True:
        ret, frame = VIDEO.read()
        print(frame)
        if frame is None:
            continue
        if ret:
            print("retting..")
            for y in range(MIDDLE-10, MIDDLE+10):
                print(y)
                for x in range(10):
                    frame[y, x, :] = 0
        else:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break

def encode():
    pass

def decode():
    pass

print("getting square...")
getSquare()
print("all done!")




