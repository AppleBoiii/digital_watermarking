import cv2
import numpy as np
import pandas as pd

VIDEO = cv2.VideoCapture("test-tube.mp4")
WIDTH = int(VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT))
MIDDLE = (int)(HEIGHT/2)
FPS = VIDEO.get(cv2.CAP_PROP_FPS)
LENGTH = VIDEO.get(cv2.CAP_PROP_FRAME_COUNT)

ENC_NAME = "crop_encoded.avi"
#ENC_VIDEO = cv2.VideoCapture("encoded.avi")

def getFrameBrightness(img=None):
    sum_pixels = img.sum()
    brightness = sum_pixels / HEIGHT / WIDTH

    return brightness

def getPreEncodedBrightness():
    #MP42 for mp4
    #DIVX for avi
    video_writer = cv2.VideoWriter("empty_encoded.avi",cv2.VideoWriter_fourcc(*'DIVX') , FPS, (WIDTH, HEIGHT))
    pre_saved_brightness = []

    while(True):
        ret, frame = VIDEO.read()
        # print(ret)
        if ret:
            # pre_saved_brightness = []
            brightness = getFrameBrightness(frame)
            pre_saved_brightness.append(brightness)
            video_writer.write(frame)
        else:
            break
    
    video_writer.release()
    VIDEO.release()
    print("Success!")

    return pre_saved_brightness

def getEmptyEncodedBrightness():
    encoded_brightness = []
    empty_video = cv2.VideoCapture("empty_encoded.avi")

    while(True):
        ret, frame = empty_video.read()
        if ret:
            brightness = getFrameBrightness(frame)
            encoded_brightness.append(brightness)

        else:
            break
        
    empty_video.release()
    return encoded_brightness

def compareBrightness(pre_saved_brightness , encoded_brightness):
    diffs = []
    for i in range(len(pre_saved_brightness)):
        diff = abs(pre_saved_brightness[i]-encoded_brightness[i])
        diffs.append(diff)
        print(f"frame: {i} diff: {diff}")
    
    n = max(diffs)
    return n

def binaryString(msg): #takes the message and returns the binary version of it
	output = ""

	for letter in msg:
		output += (bin(letter)[2:].zfill(8))

	return output

def getEncodedBrightness():
    enc = cv2.VideoCapture(ENC_NAME)
    while True:
        ret, frame = enc.read()
        if ret:
            brightness = int(getFrameBrightness((frame)))
            print(brightness)
        else:
            break
    enc.release()

def encode(msg, N):
    msg = list(msg)
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter(ENC_NAME, cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into
    frame_count = 0
    while(True):
        ret, frame = VIDEO.read()

        '''
        keep adding into frame by intervals of +1 until brightness is preferred value, then write it to writer
        '''
        if ret:
            print(frame_count)
            try:
                bit = msg.pop(0)
                brightness = int(getFrameBrightness(frame))

                remainder = brightness % N

                lower = brightness - remainder
                upper = brightness + (N-remainder)

                oddMultiple, evenMultiple = 0,0

                if lower%2 == 0:
                    evenMultiple = lower
                    oddMultiple = upper
                else:
                    evenMultiple = upper
                    oddMultiple = lower
                
                post_brightness = int(brightness)
                if bit == "1":
                    if oddMultiple < post_brightness:
                        z = -1
                        while oddMultiple < post_brightness:
                            frame = cv2.add(frame, z)
                            # print(f"{oddMultiple} : {post_brightness} : {z} ")
                            post_brightness = int(getFrameBrightness(frame))
                            z += -1
                    else:
                        z = 1
                        while oddMultiple > post_brightness:
                            # print(f"{oddMultiple} : {post_brightness} : {z} ")
                            frame = cv2.add(frame, z)
                            post_brightness = int(getFrameBrightness(frame))
                            z += 1
                else:
                    if evenMultiple < post_brightness:
                        z = -1
                        while evenMultiple < post_brightness:
                            frame = cv2.add(frame, z)
                            # print(f"{evenMultiple} : {post_brightness} : {z} ")
                            post_brightness = int(getFrameBrightness(frame))
                            z += -1
                    else:
                        z = 1
                        while evenMultiple > post_brightness:
                            # print(f"{evenMultiple} : {post_brightness} : {z} ")
                            frame = cv2.add(frame, z)
                            post_brightness = int(getFrameBrightness(frame))
                            z += 1
            except:
                pass        
            
            encodedVideo.write(frame)
            frame_count += 1
        else:
            break
    VIDEO.release()
    encodedVideo.release()
    print("Success!")


def checkAccuracy(msg, decoded_msg):
    wrong_count = 0
    for bit in range(len(msg)):
        if msg[bit] != decoded_msg[bit]:
            wrong_count += 1

    print(wrong_count)

def decode(N, msgLength):
    decodedMessageBinary = ""
    enc = cv2.VideoCapture(ENC_NAME)
    frame_count = 0
    while True:
        ret, frame = enc.read()
        if len(decodedMessageBinary) < msgLength:
            brightness = int(getFrameBrightness(frame))
            x = brightness / N
            x = round(x)

            if x%2 == 0:
                decodedMessageBinary += "0"
            else:
                decodedMessageBinary += "1"
        else:
            break
        frame_count += 1

    msg = ""

    for letter in decodedMessageBinary:
        if letter == "1":
            msg += "0"
        else:
            msg += "1"
    print(decodedMessageBinary)
    return decodedMessageBinary
    print(msg)
    return msg

n = 17
msg = binaryString(b"hi im josh im cool")
x = len(msg)
print(x)
print(msg)

# encode(msg, n)
print("decoding...")
decoded_msg = decode(n, x)
print("Done!")

checkAccuracy(msg, decoded_msg)

