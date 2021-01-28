import cv2 
import numpy as np
from numpy.core.shape_base import block
import pandas as pd
import math

SIZE_OF_BLOCK = 8

VIDEO = "test-tube.mp4"
VIDEO = cv2.VideoCapture(VIDEO)

NUM_OF_FRAMES = int(VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
HEIGHT = int(VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT))
WIDTH = int(VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH))

ENCODED= "encoded.avi"
ENCODED = cv2.VideoCapture(ENCODED)
ENC_NUM_OF_FRAMES = int(ENCODED.get(cv2.CAP_PROP_FRAME_COUNT))

def brightness(x=int(512/2), y=int(512/2), img=None):
    if img is None:
        print("No image found.")
        return 0
    
    brightness = (sum(img[y, x, :]))/3 #average of BGR values = brightness
    return int(brightness)

def brightnessBlock(img):
    if img is None:
        print("No image found.")
        return 0
    
    avg_pixel_brightness = []
    for j in range(len(img)):
        for k in range(len(img)):
            pixel_brightness = (sum(img[j, k, :]))/3
            avg_pixel_brightness.append(pixel_brightness)

    block_brightness = (sum(avg_pixel_brightness))/(len(avg_pixel_brightness))

    return block_brightness

''' 
getBlockBrightness():
gets an 8x8, 16x16 or something block of pixels from the image.
need to be able to get the brightness of this block, and compare it the equivalent of the encoded block.
'''

def getBlocksBrightness(vid_frame, enc_frame):
    NUM_OF_SQUARES = (int)((HEIGHT * WIDTH) / (SIZE_OF_BLOCK*SIZE_OF_BLOCK))
    x, y = SIZE_OF_BLOCK, SIZE_OF_BLOCK
    squares_brightness = []
    SQUARE_COUNT = 0
    while SQUARE_COUNT != NUM_OF_SQUARES:
        norm_square = vid_frame[(y-SIZE_OF_BLOCK):y, (x-SIZE_OF_BLOCK):x, :]
        enc_square = enc_frame[(y-SIZE_OF_BLOCK):y, (x-SIZE_OF_BLOCK):x, :]

        norm_square_brightness = brightnessBlock(norm_square)
        enc_square_brightness = brightnessBlock(enc_square)

        squares_brightness.append([[norm_square_brightness, ""], [enc_square_brightness]])
        SQUARE_COUNT += 1
        
        if x >= WIDTH:
            y += SIZE_OF_BLOCK
            x = SIZE_OF_BLOCK
        else:
            x += SIZE_OF_BLOCK
    
    return squares_brightness

data = []
frame_count = 0
while(True):
    vid_ret, vid_frame = VIDEO.read()
    enc_ret, enc_frame = ENCODED.read()

    if vid_ret:
        
        if frame_count == 75:
            data = getBlocksBrightness(vid_frame, enc_frame)

            #for getting individual pixel brightness
            # for y in range(HEIGHT):
            #     for x in range(WIDTH):
            #         vid_pixel_brightness = brightness(x, y, vid_frame)
            #         enc_pixel_brightness = brightness(x, y, enc_frame)

            #         data.append([[vid_pixel_brightness, enc_pixel_brightness], [vid_pixel_brightness/enc_pixel_brightness]])

        frame_count += 1
        if frame_count > 75:
            break


arr = np.array(data)
df = pd.DataFrame(arr, columns = ["1", "2"])

df.to_csv(f"brightness_comparisons_{SIZE_OF_BLOCK}x{SIZE_OF_BLOCK}.csv")
print("Excel sheet saved.")