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

def decodeTest(y):
    N = 11

    remainder = y%N
    lowerMultiple = y-remainder
    upperMultiple = y+(N-remainder)
    x = 0

    #figure out what to do when its less than 8
    if y - lowerMultiple > upperMultiple - y:
        x = upperMultiple
    
    else:
        x = lowerMultiple
    
    print(x)

    x /= N

    print(x)

def encodeTest(y):
    N = 11
    remainder = y % N

    lower = y - remainder
    upper= y + (N-remainder)

    oddMultiple, evenMultiple = 0,0

    if lower%2 == 0:
        evenMultiple = lower
        oddMultiple = upper
    else:
        evenMultiple = upper
        oddMultiple = lower

    
    print(evenMultiple)    
    numberToAdd = oddMultiple - y
    numbertoAdd2 = evenMultiple - y

    print(numberToAdd)
    print(numbertoAdd2)

while(True):
    x = input("Yes: ")
    x = float(x)
    x = int(x)
    encodeTest(x)




# img = cv2.imread("Lenna.png")
# view = np.uint8([255, 255, 255])
# y = np.uint8([10])
# print(view)
# view = cv2.add(view, -1.4)
# print(view)

'''
92.4
x = (int)(92.4)
x = 92, make this 90

87 - 93 

90 / 5 = 17 - 18 --> 0
90 / 4 = 22.5




51 and 0
92 and 1

TO ENCODE:
On even blocks, use four. On odd blocks, use five. 
If the bit is a 1, change the brightness to the nearest odd multiple of 4 or 5 
If the bit is 0, change the brightness to the nearest even multiple of 4 or 5

92 -> 90

90/5 = 18

87/5 = 17.4
93/5 = 18.6

N = 5

if block%2 == 0:
    N = 4

bit = bit_array.pop()

brightness = getBrightness()
remainder = brightness % N

lowerMultiple = brightness - remainder
upperMultiple = brightness + (N-remainder)

oddMultiple = 0
evenMultiple = 0

if lower%2 == 0:
    evenMultiple = lowerMultiple
    oddMultiple = upperMultiple
else:
    evenMultiple = upperMultiple
    oddMultiple = lowerMultiple

if bit == 1:
    numberToAdd[:, :] = oddMultiple - brightness

    img[:, :] = cv2.add(img, numberToAdd)
else:
    numberToAdd[:, :] = evenMultiple - brightness

    img[:, :] = cv2.add(img, numberToAdd)



TO DECODE:
Divide brightness by N and make int. If even make 0. If odd make 1.

N = 5
if block%2 == 0:
    N = 4

brightness = getBrightness()
num = (int)(brightness/N)
if num % 2 == 0:
    message += 0
else:
    num % 2 == 1
'''
 

