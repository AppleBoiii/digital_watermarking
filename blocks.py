import pandas as pd
import numpy as np


FILE_NAME = "brightness_comparisons_16x16_frames1-50.csv"
class Blocks:
    def __init__(self, FILE_NAME="brightness_comparisons_16x16_frames1-50.csv"):
        self.name = FILE_NAME
        self.data = pd.read_csv(self.name)
        self.list_of_special_blocks = self.getSpecialBlocks()

    def getSpecialBlocks(self):
        specialBlocks = []

        for i in range(len(self.data.columns)):
            k = str(i)
            column = self.data[[k]]
            tempList = []
            for j in range(len(self.data.index)):
                if column.iloc[j].item() <= 1.8:
                    tempList.append(j)

            specialBlocks.append(tempList)
        
        specialBlocks = np.array(specialBlocks)
        return specialBlocks


# data = Blocks()
# print(data.list_of_special_blocks[49])
# print("...\n")
# # print(special_blocks)


'''
the goal of this file is to be able to be inputed any amount of frames, with the difference between pre-ouput and output videos
so that where the difference is extremely small (<=1.8) can be recorded and sent to the file that does the encoding. I hope this will
make it possible to encode very small changes in brightness with strong encoding.

need list in format -> [frame][blocks]
go through every column, append ones that are <=1.8
so list[0][x] accesses every column in the first frame
'''
