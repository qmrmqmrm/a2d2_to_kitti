#!/home/dolphin/.pyenv/versions/open3d/pin/python



import os
import glob
import json
import cv2
import open3d as o3d
import numpy as np
import pprint
import load_and_save as f


def drow_box(img, bboxes):
    print(img)
    img = cv2.imread(img)
    drow = img.copy()
    for bbox in bboxes:
        print(bbox)
        drow = cv2.rectangle(drow,(int(bbox[0]),int(bbox[1])),(int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3])),(255,255,255),2)
    cv2.imshow("img", img)
    cv2.imshow("drow", drow)
    cv2.waitKey(0)



if __name__ == '__main__':
    root = '/media/dolphin/intHDD/birdnet_data/bv_a2d2/annotations'
    annotations = f.load_json(root)
    img_file_name = annotations[0].get("images")[0].get("file_name")
    label_file_name = img_file_name.split("/")[-1].split(".")[0]
    file_name_bboxes = os.path.join("/".join(img_file_name.split('/')[:-2]),"label",
                                    label_file_name+".txt")
    label = f.load_txt(file_name_bboxes)
    print(annotations[0].get("annotations")[0])
    bboxes =list()
    for i in range(3):
        bbox = (annotations[0].get("annotations"))[i].get("bbox")
        bboxes.append(bbox)
    print(bboxes)
    # drow_box(img_file_name,bbox)
    drow_box(img_file_name, bboxes)
