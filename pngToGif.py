import sys, os, math, datetime
import numpy as np
import random as rd
import time

from PIL import Image
import glob
import imageio

if __name__ == "__main__":

    nameCommon = "Slide";

    '''
    #does not support transparency
    inputPath = os.getcwd() + "/figures/" + nameCommon + "*.png";
    imgNames = glob.glob(inputPath);
    imgs = [];
    for imgName in imgNames:
        imgs.append(imageio.imread(imgName));
    outputPath = os.getcwd() + "/figures/" + nameCommon + ".gif";
    imageio.mimsave(outputPath, imgs, duration=0.5, quantizer=0);
    '''

    inputPath = os.getcwd() + "/figures/" + nameCommon + "*.png";
    imgNames = sorted(glob.glob(inputPath));
    imgs = []
    transparency = "";
    for imgName in imgNames:
        frame = Image.open(imgName);
        frame = frame.convert("RGBA");
        imgs.append(frame);

    outputPath = os.getcwd() + "/figures/" + nameCommon + ".gif";
    imgs[0].save(outputPath, save_all=True, format='GIF',
                 append_images=imgs[1:], transparency=0,
                 duration=200, disposal=2, loop=0);






 
