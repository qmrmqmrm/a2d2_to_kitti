#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import cv2
import json

import bounding_boxes as a2


def merge_to_all_image(path):


    img = cv2.imread(path)
    img = cv2.line(img,(0,700),(1400,700),(255,255,255),1)
    img = cv2.line(img,(0,1400),(1400,1400),(255,255,255),1)
    save_ = '/media/dolphin/intHDD/birdnet_data/result_image/000044767.png'
    cv2.imwrite(save_,img)


if __name__ == '__main__':

    path = '/media/dolphin/intHDD/birdnet_data/bv_a2d2/result/ckpt/final/vlog/ep13/total_img/20181204_170238/image/000044767.png'
    merge_to_all_image(path)