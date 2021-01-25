import cv2
import numpy as np
import math 


VIDEO_NAME = input("Gimme video name + file extension: ")
ENCODED_NAME = input("give desired name of encoded video (rn only .avi extensions work: ")

#gets width, height, and middle-height of the image
VIDEO = cv2.VideoCapture(VIDEO_NAME)
WIDTH = VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH)
WIDTH = (int)(WIDTH)
HEIGHT = VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT) 
HEIGHT = (int)(HEIGHT)
MIDDLE = (int)(HEIGHT/2)

def sinFunc(x): #function to type instead of typing out this sinusoid 
    y = (int(MIDDLE+(75*math.sin(x)))) 
    return y

def binaryString(msg): #takes the message and returns the binary version of it
	output = ""

	for letter in msg:
		output += (bin(letter)[2:].zfill(8))

	return output

def brightness(x=int(512/2), y=int(512/2), img=None):
    if img is None:
        print("No image found.")
        return 0
    
    brightness = (sum(img[y, x, :]))/3 #average of BGR values = brightness
    return int(brightness)

def encode(msg):
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter(ENCODED_NAME, cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into
    msg = list(msg)

    while(True):
        ret, frame = VIDEO.read()

        if ret:
            for x in range(WIDTH):
                y = sinFunc(x)

                try:
                    bit = msg.pop(0)             #odd pixels = 1, even pixels = 0
                    if brightness(x, y, frame)%2==0 and bit=="1": 
                        frame[y, x, :] += 1
                    elif brightness(x, y, frame)%2==1 and bit=="0":
                        frame[y, x, :] += 1
                except:
                    continue

            encodedVideo.write(frame)
        else:
            break
    
    VIDEO.release()
    encodedVideo.release()
    print("Success!")
    cv2.destroyAllWindows()

def decode(videoFileName):
    try:
        encoded = cv2.VideoCapture(videoFileName)
    except:
        print("Video not found.")
        return 0
    
    encodedWidth = (int)(encoded.get(cv2.CAP_PROP_FRAME_WIDTH))
    decodedMessageBinary = ""

    while(True):
        ret, frame = encoded.read()

        if frame is None:
            continue

        for x in range(encodedWidth):
            y = sinFunc(x) #used to find the same pixels that were encoded
        
            try:                               #odd pixels = 1, even pixels = 0
                if brightness(x, y, frame)%2 == 0:
                    decodedMessageBinary += "0"
                else:
                    decodedMessageBinary += "1"
        
            except:
                continue
        
        break
    
    print(decodedMessageBinary)



msg = binaryString(b"boof")
print(msg)

#encode(msg)
print("\n")

print("decoding...")
decode(ENCODED_NAME)

#imgDecode()