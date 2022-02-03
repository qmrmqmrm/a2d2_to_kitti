#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import shutil
import math
import cv2

import get_calibration_form as gc
import bounding_boxes as a2
import load_and_save as sf


def trim_empty_anno_frames(root_path):
    folders_train = []
    # '20180807_145028', '20180810_142822', '20180925_101535', '20180925_112730',
    #  '20180925_124435', '20180925_135056', '20181008_095521', '20181016_125231',
    #  '20181107_132300', '20181107_132730', '20181107_133258', '20181108_084007',
    #  '20181108_091945', '20181108_103155', '20181108_123750']

    img_1_path = root_path+"/testing/000006660_max_height.png"
    img_2_path = root_path+ "/testing_3/000006660_max_height.png"
    print(root_path)
    print(img_2_path)
    img_1 = cv2.imread(img_1_path)
    img_2 = cv2.imread(img_2_path)
    img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY) * 255
    img_2 = cv2.cvtColor(img_2, cv2.COLOR_GRAY2BGR)

    img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY) * 255
    img_1 = cv2.cvtColor(img_1, cv2.COLOR_GRAY2BGR)
    cv2.imshow('img_1',img_1)
    cv2.imshow('img_2', img_2)

    cv2.waitKey(0)



if __name__ == "__main__":
    RESULT_ROOT = "/media/dolphin/intHDD/kim/new_img"
    trim_empty_anno_frames(RESULT_ROOT)
