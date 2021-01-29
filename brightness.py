import cv2
import numpy as np
import math 


# VIDEO_NAME = input("Gimme video name + file extension: ")
VIDEO_NAME = "test-tube.mp4"
# ENCODED_NAME = input("give desired name of encoded video (rn only .avi extensions work: ")
ENCODED_NAME = "encoded.avi"

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

FRAME_COUNT = 40
BLOCK_VALUES = [2824, 2739, 2817, 2562]
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
def getBrightnessOfBlocks(block):
    avg_pixel_brightness = []
    for j in range(len(block)):
        for k in range(len(block)):
            pixel_brightness = (sum(block[j, k, :]))/3
            avg_pixel_brightness.append(pixel_brightness)

    block_brightness = (sum(avg_pixel_brightness))/(len(avg_pixel_brightness))

    return block_brightness

def getBlocks(vid_frame):
    global NUM_OF_BLOCKS
    BLOCK_COUNT = 0
    x, y = SIZE_OF_BLOCK, SIZE_OF_BLOCK
    block_brightness_list = []

    while BLOCK_COUNT != NUM_OF_BLOCKS:
        norm_block = vid_frame[(y-SIZE_OF_BLOCK):y, (x-SIZE_OF_BLOCK):x, :]

        norm_block_brightness = getBrightnessOfBlocks(norm_block)

        block_brightness_list.append([norm_block, norm_block_brightness])
        BLOCK_COUNT += 1
        
        if x >= WIDTH:
            y += SIZE_OF_BLOCK
            x = SIZE_OF_BLOCK
        else:
            x += SIZE_OF_BLOCK
    
    return block_brightness_list


'''
I use this to break the org video into frames and re-stich it back together and save into new file
so I can later see how much the pixels changed by the video compression. 
Theoretically if i know how much they change by compression I can sort-of plan how I want to encode into the 
original file. 
'''
def emptyEncode():
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter(ENCODED_NAME, cv2.VideoWriter_fourcc(*'DIVX') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into
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

def encode(msg):
    msg = list(msg)
    #MP42 for mp4
    #DIVX for avi
    encodedVideo = cv2.VideoWriter(ENCODED_NAME, cv2.VideoWriter_fourcc(*'MP42') , 25, (WIDTH, HEIGHT)) #video writer object to store modified frames into

    frame_num = 0

    while(True):
        ret, frame = VIDEO.read()
        '''
        Between frames 40 - 43, I want to encode 8 bits of data in the specific macroblocks I listed in the array above at the top of 
        my code. i specifies the index of that array, so there are different macroblocks for different frames. i changes depending on the frame
        the video is on. 
        '''
        if ret:
            if FRAME_COUNT <= frame_num <= FRAME_COUNT+3:
                blocks = getBlocks(frame) #gets all the NxN blocks in this frame 
                if frame_num == 40:
                    i = 0
                elif frame_num == 41:
                    i = 1
                elif frame_num == 42:
                    i = 2
                else:
                    i = 3
                for block in range(len(blocks)):
                    if block in range(BLOCK_VALUES[i]-8, BLOCK_VALUES[i]):
                    # if BLOCK_VALUES[i]-7 <= block <= BLOCK_VALUES[i]:
                        print(i)
                    # try:
                        N = 7

                        # if block%2 == 0:
                        #     N = 13

                        bit = msg.pop()

                        '''
                        Basically, I take the brightness of the block and get the remainder of it divided by N. If the bit I want to encode is a 0 
                        or 1 depends what I do next. If 0, I want to store it in the nearest even multiple of N. If 1, the nearest odd multiple of N.
                        So I want to do some math to figure out which multiple is which, and change the brightness to that value accordingly. 

                        ''' 

                        brightness = int(blocks[block][1])
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

                        if bit == 1:
                            numberToAdd = oddMultiple - brightness

                            '''
                            I feel like this may be working right. 
                            '''
                            frame[:, :] = cv2.add(frame, numberToAdd)
                        else:
                            numberToAdd = evenMultiple - brightness

                            frame[:, :] = cv2.add(frame, numberToAdd)

                        # except:
                        #     print("Something went wrong.")
                        #     continue

            encodedVideo.write(frame)
            frame_num += 1
            # print(frame_count)
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
    
    decodedMessageBinary = ""
    frame_num = 0

    while(True):
        ret, frame = encoded.read()

        if ret:
            if FRAME_COUNT <= frame_num <= FRAME_COUNT+3:
                blocks = getBlocks(frame)
                for block in range(len(blocks)):
                    if frame_num == 40:
                        i = 0
                    elif frame_num == 41:
                        i = 1
                    elif frame_num == 42:
                        i = 2
                    else:
                        i = 3
                    if block in range(BLOCK_VALUES[i]-8, BLOCK_VALUES[i]):
                        N = 7
                        # if block%2 == 0:
                        #     N = 13

                        '''
                        brightness only changes by a max of -5 or +4
                        so if use 12 or 13, then can figure out waht its meant to be
                        ex. brightness = 14, well if that is encoded then it was encoded to be 12 not 24
                        bc the pixels would not change by 10. 
                        so correct the brightness and get the 1 or 0 out. 
                        '''
                        brightness = int(blocks[block][1])
                        remainder = int(brightness%N)
                        lowerMultiple = brightness-remainder
                        upperMultiple = brightness+(N-remainder)
                        x = 0

                        #figure out what to do when its less than 8
                        if brightness - lowerMultiple > upperMultiple - brightness:
                            x = upperMultiple
                        
                        else:
                            x = lowerMultiple
                        
                        #x /= N

                        if x%2 == 0:
                            decodedMessageBinary += "0"
                        else:
                            decodedMessageBinary += "1"

                    # if block > 0 and block%32==0:
                    #     if count == 22:
                    #         binaryList.append([decodedMessageBinary, block])
                    #     decodedMessageBinary = ""
                    #     count += 1
            frame_num += 1
        else:
            break

    #print(binaryList[0])
    print(decodedMessageBinary)


#remember first 8 bits and 22th byte
#704 block best blocks to do stuff on


msg = binaryString(b"hihi")
print(f"The message is {msg}")
print(len(msg))

# encode(msg)
# # print("\n")

print("decoding...")
decode(ENCODED_NAME)

#imgDecode()
