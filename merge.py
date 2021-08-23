#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import cv2
import json

import get_calibration_form as gc
import bounding_boxes as a2
import load_and_save as sf


def merge_to_all_image(root_path):
    calibriation_dict = gc.get_calibration(root_path)
    camera_file_names = sorted(
        glob.glob(os.path.join(root_path, 'bbox/camera_lidar_semantic_bboxes/*/camera/cam_front_center/*.png')))

    save_dirctory = "/media/dolphin/intHDD/birdnet_data/my_a2d2"
    save_camera_dirctory = os.path.join(save_dirctory, 'camera')
    save_label_dirctory = os.path.join(save_dirctory, 'label')

    num_list = list()
    num_files = len(camera_file_names)

    for i, camera_file_name in enumerate(camera_file_names):
        seq_name = camera_file_name.split('/')[-1]
        file_name = seq_name.split('.')[0]
        file_num = file_name.split('_')[-1]
        # num_list.append(file_num)

        img = cv2.imread(camera_file_name)
        save_camera = os.path.join(save_camera_dirctory,f"{file_num}.png")
        # print(save_camera)
        cv2.imwrite(save_camera,img)

        # # file_name_bboxes = extract_bboxes_file_name_from_image_file_name(lidar_file_name)
        # file_name_bboxes = seq_name.replace("camera_","label3D_").replace("png","json")
        # file_name_bboxes = os.path.join("/".join(camera_file_name.split('/')[:-3]), "label3D", "cam_front_center",
        #                                 file_name_bboxes)
        # # print(file_name_bboxes)
        # save_label = os.path.join(save_label_dirctory,f"{file_num}.json")
        # boxes = a2.read_bounding_boxes(file_name_bboxes)
        # with open(save_label,"w") as make_file:
        #     json.dump(boxes, make_file, indent="\t")
        # lines = a2.convert_a2d2_to_kitti_label(boxes)

        print_progress(f"-- Progress: {i}/{num_files}")




def print_progress(status_msg):
    # NOTE: the \r which means the line should overwrite itself.
    msg = "\r" + status_msg
    # Print it.
    sys.stdout.write(msg)
    sys.stdout.flush()


if __name__ == '__main__':
    root_path = '/media/dolphin/intHDD/a2d2'
    convert_a2d2_to_kitti(root_path)
