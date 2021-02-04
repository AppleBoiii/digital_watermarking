import cv2
import numpy as np
import pandas as pd

# VIDEO_NAME = input("Gimme video name + file extension: ")
VIDEO_NAME = "test-tube.mp4"
# ENCODED_NAME = input("give desired name of encoded video (rn only .avi extensions work: ")
ENCODED_NAME = "encoded1.avi"

#gets width, height, and middle-height of the image
VIDEO = cv2.VideoCapture(VIDEO_NAME)
WIDTH = VIDEO.get(cv2.CAP_PROP_FRAME_WIDTH)
WIDTH = (int)(WIDTH)
HEIGHT = VIDEO.get(cv2.CAP_PROP_FRAME_HEIGHT) 
HEIGHT = (int)(HEIGHT)
MIDDLE = (int)(HEIGHT/2)

N = 16
SIZE_OF_BLOCK = N
NUM_OF_BLOCKS = (int)((HEIGHT * WIDTH) / (SIZE_OF_BLOCK*SIZE_OF_BLOCK))

FRAME_COUNT = 50
BLOCK_VALUES = [2823, 2739, 2817, 2562]
BLOCK_VALUES = np.array(BLOCK_VALUES)

def binaryString(msg): #takes the message and returns the binary version of it
	output = ""

	for letter in msg:
		output += (bin(letter)[2:].zfill(8))

	return output

def getBrightness(x=int(512/2), y=int(512/2), img=None):
    if img is None:
        print("No image found.")
        return 0
    
    brightness = (sum(img[y, x, :]))/3 #average of BGR values = brightness
    return int(brightness)


'''
these two functions work together
get blocks returns a list of all the NxN blocks of the video, as well as the overall brightness of those blocks
'''

def getBlockBrightness(coords, frame):
    brightnessList = []
    x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]

    for y in range(y1, y2):
        for x in range(x1, x2):
            brightnessList.append(getBrightness(x,y, frame))
    
    sumOfBrightness = sum(brightnessList)
    avgBrightness = sumOfBrightness / len(brightnessList)

    return int(avgBrightness)

def getBlocks(frame):
    global NUM_OF_BLOCKS
    global SIZE_OF_BLOCK
    x, y = SIZE_OF_BLOCK, SIZE_OF_BLOCK
    block_count = 0

    block_list = []

    while block_count != NUM_OF_BLOCKS:
        block_list.append([x-SIZE_OF_BLOCK, y-SIZE_OF_BLOCK, x, y])

        block_count += 1
        if x >= WIDTH:
            y += SIZE_OF_BLOCK
            x = SIZE_OF_BLOCK
        else:
            x += SIZE_OF_BLOCK
    
    #print(len(block_list))
    return block_list

def getBlocksThatChangeTheLeast(file_name="brightness_comparisons_16x16_frames1-50.csv"):
    data = pd.read_csv(file_name)
    specialBlocks = []

    for i in range(len(data.columns)): #goes through every column
        k = str(i)
        column = data[[k]]  #get the current column 
        tempList = []
        for j in range(len(data.index)):    #go through every single row of that column
            if column.iloc[j].item() < 2:    #if the elem @ column is certain value, append it
                tempList.append(j)

        specialBlocks.append(tempList)
    
    # arr = np.asarray(specialBlocks)
    return specialBlocks

'''
I use this to break the org video into frames and re-stich it back together and save into new file
so I can later see how much the pixels changed by the video compression. 
Theoretically if i know how much they change by compression I can sort-of plan how I want to encode into the 
original file. 
'''
def emptyEncode():
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter("empty_encoded.avi", cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into
    while(True):
        ret, frame = VIDEO.read()
        if ret:
            encodedVideo.write(frame)
        else:
             break
    
    VIDEO.release()
    encodedVideo.release()
    print("Success!")
    cv2.destroyAllWindows()

def encode(msg, arr):
    msg = list(msg)
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter(ENCODED_NAME, cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into

    frame_num = 0 #keeps count of frames
    # a = 0

    while(True):
        ret, frame = VIDEO.read()

        if ret:
            if 1 <= frame_num <= len(arr)-1:
                blocks = getBlocks(frame) #gets all the NxN blocks in this frame 

                for block in blocks:
                    z = blocks.index(block)
                    if z in arr[frame_num]:
                        
                        try:
                            # print(a)
                            bit = msg.pop()
                            # a+=1
                        except:
                            break

                    
                        x1, y1, x2, y2 = block[0],block[1], block[2], block[3]

                        N = 7

                        brightness = getBlockBrightness([x1, y1, x2, y2], frame)
                        remainder = brightness % N

                        lower = brightness - remainder
                        upper= brightness + (N-remainder)

                        oddMultiple, evenMultiple = 0,0

                        if lower%2 == 0:
                            evenMultiple = lower
                            oddMultiple = upper
                        else:
                            evenMultiple = upper
                            oddMultiple = lower

                        if bit == "1":
                            numberToAdd = oddMultiple - brightness
                            if numberToAdd < 0:
                                frame[y1:y2, x1:x2, :] -= abs(numberToAdd)
                            else:
                                frame[y1:y2, x1:x2, :] += numberToAdd

                        else:
                            numberToAdd = evenMultiple - brightness
                            if numberToAdd < 0:
                                frame[y1:y2, x1:x2, :] -= abs(numberToAdd)
                            else:
                                frame[y1:y2, x1:x2, :] += numberToAdd

            encodedVideo.write(frame)
            frame_num += 1
        else:
            break
    
    VIDEO.release()
    encodedVideo.release()
    print("Success!")
    cv2.destroyAllWindows()

def decode(videoFileName, arr):
    try:
        encoded = cv2.VideoCapture(videoFileName)
    except:
        print("Video not found.")
        return 0
    
    decodedMessageBinary = ""
    # msgList = []
    frame_num = 0

    while(True):
        ret, frame = encoded.read()

        if ret:
            if 1 <= frame_num <= len(arr)-1:
                blocks = getBlocks(frame)

                for block in blocks:
                    z = blocks.index(block)
                    if z in arr[frame_num]:
                        if len(decodedMessageBinary) >= 48:
                            # msgList.append(decodedMessageBinary)
                            # decodedMessageBinary = ""
                            break

                        N = 7
                        x1 = block[0]
                        y1 = block[1]
                        x2 = block[2]
                        y2 = block[3]

                        brightness = getBlockBrightness([x1, y1, x2, y2], frame)
                        remainder = int(brightness%N)
                        lowerMultiple = brightness-remainder
                        upperMultiple = brightness+(N-remainder)
                        x = 0

                        if brightness - lowerMultiple > upperMultiple - brightness:
                            x = upperMultiple
                        
                        else:
                            x = lowerMultiple
                        
                        
                        x /= N

                        if x%2 == 0:
                            decodedMessageBinary += "0"
                        else:
                            decodedMessageBinary += "1"

            frame_num += 1
        else:
            break
        
    # for msg in msgList:
    #     msg = msg[::-1]
    
    # print(msgList)
    decodedMessageBinary = decodedMessageBinary[::-1]
    # print(decodedMessageBinary)
    return decodedMessageBinary
    # return msgList


arr = getBlocksThatChangeTheLeast()

'''
if 1 <= frame_count <= len(arr)-1:
'''


msg = binaryString(b"secret") #the result of this is 1 bit off. 
# print(f"The message is {msg}")
# print(len(msg))
# encode(msg, arr)
# print("\n")
print("decoding...")
decoded = decode(ENCODED_NAME, arr)
print(decoded)
# if msg in decoded:
#     print(True)
#     print(msg)

'''
no worky, try idea:
encode whole image or very large squares sof image, that way watermark can't be cropped out
'''