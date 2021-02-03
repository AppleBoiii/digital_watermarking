import pandas as pd
import numpy as np
import csv

FILE_NAME = "brightness_comparisons_16x16_frames1-50.csv"

def getCSV():
    data = pd.read_csv(FILE_NAME)

    return data

def getSpecialBlocks(data):
    specialBlocks = []

    for i in range(len(data.columns)):
        k = str(i)
        column = data[[k]]
        tempList = []
        for j in range(len(data.index)):
            if column.iloc[j].item() <= 1.8:
                tempList.append(j)

        specialBlocks.append(tempList)
    
    specialBlocks = np.array(specialBlocks)
    return specialBlocks

data = getCSV()
special_blocks = getSpecialBlocks(data)
special_blocks = pd.DataFrame(special_blocks, columns=["0"])
# special_blocks.to_csv("special_blocks.csv")
print("...\n")
print(special_blocks)


'''
the goal of this file is to be able to be inputed any amount of frames, with the difference between pre-ouput and output videos
so that where the difference is extremely small (<=1.8) can be recorded and sent to the file that does the encoding. I hope this will
make it possible to encode very small changes in brightness with strong encoding.

need list in format -> [frame][blocks]
go through every column, append ones that are <=1.8
so list[0][x] accesses every column in the first frame
'''
