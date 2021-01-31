import cv2 
import numpy as np
import pandas as pd
import math

SIZE_OF_BLOCK = 16

VIDEO = "test-tube.mp4"
VIDEO = cv2.VideoCapture(VIDEO)

NUM_OF_FRAMES = int(VIDEO.get(cv2.CAP_PROP_FRAME_COUNT))
HEIGHT = int(VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT))
WIDTH = int(VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH))

ENCODED= "empty_encoded.avi"
ENCODED = cv2.VideoCapture(ENCODED)
ENC_NUM_OF_FRAMES = int(ENCODED.get(cv2.CAP_PROP_FRAME_COUNT))

FRAME_COUNT = 50

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

        abs_diff = abs(norm_square_brightness-enc_square_brightness)
        squares_brightness.append(abs_diff)
        SQUARE_COUNT += 1
        
        if x >= WIDTH:
            y += SIZE_OF_BLOCK
            x = SIZE_OF_BLOCK
        else:
            x += SIZE_OF_BLOCK
    
    return squares_brightness

def getData(frame):
    frame_count = 0
    data_list = []
    while(True):
        vid_ret, vid_frame = VIDEO.read()
        enc_ret, enc_frame = ENCODED.read()
        if vid_ret:
            if frame_count in range(1, frame+1):     #getting 50 frames
                if not frame_count % 5:
                    print(frame_count)
                data = getBlocksBrightness(vid_frame, enc_frame)
                data_list.append(data)

            if frame_count == frame+1:
                break
            frame_count += 1
    return data_list

print("Starting...")
arr = np.array(getData(FRAME_COUNT))
df = pd.DataFrame(arr)
df = df.transpose() #flips columns and rows
print(df)

df.to_excel(f"brightness_comparisons_{SIZE_OF_BLOCK}x{SIZE_OF_BLOCK}_frame{FRAME_COUNT}.xlsk")
print("Excel sheet saved.")