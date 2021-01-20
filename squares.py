import cv2
import numpy as np
import math

# VIDEO_NAME = input("Gimme video name + file extension: ")
VIDEO_NAME = "test-tube.mp4"
ENCODED_NAME = "encoded.avi"
#ENCODED_NAME = input("give desired name of encoded video")

#gets width, height, and middle-height of the image
VIDEO = cv2.VideoCapture(VIDEO_NAME)
WIDTH = (int)(VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = (int)(VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT))
MIDDLE = (int)(HEIGHT/2)

#fps and nums of frames if needed
FPS = int(VIDEO.get(cv2.CAP_PROP_FPS))
NUM_OF_FRAMES = int(VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))


def binaryString(msg): #takes the message and returns the binary version of it
	output = ""

	for letter in msg:
		output += (bin(letter)[2:].zfill(8))

	return output

#the original function I made to test the square-ability on the videos, copied & pasted and reused for the other two funcs
def findSquares():
    FRAME_COUNT = 0
    j, k = 0, 0

    while True:
        ret, frame = VIDEO.read()
        if frame is None:
            continue

        if ret:
            COLOR = 0

            if FRAME_COUNT%1 == 0:
                j = FRAME_COUNT
                k = j+1

            for y in range(MIDDLE-10, MIDDLE+10):
                for x in range(j, k):
                    frame[y, x, :] = COLOR
        else:
            break

        cv2.imshow('frame', frame)
        FRAME_COUNT += 1
        print(FRAME_COUNT)
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break

def encode(msg):
    encodedVideo = cv2.VideoWriter(ENCODED_NAME, cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into
    msg = list(msg)

    FRAME_COUNT = 0
    COLOR = 0 #var used to determine color of square: 0 = black, 255 = white
    j, k = 0, 0 #vars used to determine x coords of the square in each frame

    while True:
        ret, frame = VIDEO.read()
        if frame is None:
            continue

        if ret:
            if FRAME_COUNT%1 == 0:
                j = FRAME_COUNT
                k = j+1

            try:
                bit = msg.pop(0)
            except:
                bit = "2"

            if bit == "1":
                COLOR = 0
            elif bit == "0":
                COLOR = 255
            else:
                pass

            for y in range(MIDDLE-10, MIDDLE+10):
                for x in range(j, k):
                    frame[y, x, :] = COLOR
        else:
            break

        # cv2.imshow('frame', frame)
        FRAME_COUNT += 1
        encodedVideo.write(frame)

        if FRAME_COUNT == NUM_OF_FRAMES:
            break
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
    
    VIDEO.release()
    encodedVideo.release()
    cv2.destroyAllWindows()

def decode():
    ENCODED_VIDEO = cv2.VideoCapture(ENCODED_NAME)

    msg = ""
    FRAME_COUNT = 0
    j, k = 0, 0

    while True:
        ret, frame = ENCODED_VIDEO.read()

        print(FRAME_COUNT)
        if ret:
            if FRAME_COUNT%1 == 0:
                j = FRAME_COUNT
                k = j + 1
            
            whiteCount = 0 #use this to count how many of pixels within the area I'm checking are a certain color
            for y in range(MIDDLE-10, MIDDLE+10):
                for x in range(j, k):
                    print(frame[y,x,:])
                    if (200 < frame[y, x, :]).all():
                        whiteCount += 1

            if whiteCount >= 1:
                msg += "0"
            else:
                msg += "1"

        FRAME_COUNT += 1
        if FRAME_COUNT == NUM_OF_FRAMES:
            break

    return msg[:176]




#getSquare()
x = binaryString(b"there is a secret here")
#encode(x)

x = decode()
print(x)





