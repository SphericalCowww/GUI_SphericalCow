import sys, os, math, datetime
import numpy as np
import random as rd
import time

from PIL import Image
import glob

if __name__ == "__main__":

    nameCommon = "cowAEdit/Slide";

    inputPath = os.getcwd() + "/figures/" + nameCommon + "*.png";
    imgNames = glob.glob(inputPath);
    for imgName in imgNames:
        if "Output" not in imgName:
            img = Image.open(imgName);
            img = img.convert("RGBA");
            data = np.array(img);
            red, green, blue, alpha = data.T;
            #print(data.T);
            background = (abs(red  -193) == 0)&\
                         (abs(blue -193) == 0)&\
                         (abs(green-193) == 0)&\
                         (abs(alpha-255) == 0);
            data[...][background.T] = (255, 255, 255, 0);
            imgOutput = Image.fromarray(data);
            imgOutput = imgOutput.save(imgName[:-4] + "Output.png");








 
