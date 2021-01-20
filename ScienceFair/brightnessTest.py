import cv2
import numpy as np
import math 

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

img = cv2.imread("Lenna.png")

# img[:, :, 0] = 255
# img[:, :, 1] = 0
# img[:, :, 2] = 0

# cv2.imshow('Lenna', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()