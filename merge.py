#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import cv2
import json

import bounding_boxes as a2


def merge_to_all_image(path):
    folders_train = ['20181108_084007',]#'20181107_132300', '20181107_132730', '20181107_133258',
                     # '20181108_091945', '20181108_103155', '20181108_123750']
                    # '20180807_145028', '20180810_142822', '20180925_101535', '20180925_112730',]
                    # '20180925_124435','20180925_135056', '20181008_095521', '20181016_125231',]

    folders_test = []  # '20181204_135952', '20181204_154421', '20181204_170238']
    splits = {'train': folders_train, 'test': folders_test}
    for split, folders in splits.items():
        num_folder = len(folders)
        for j, folder in enumerate(folders):
            camera_file_names = sorted(glob.glob(os.path.join(path, 'bbox/camera_lidar_semantic_bboxes',
                                                              folder, 'camera/cam_front_center/*.png')))

            save_dirctory = "/media/dolphin/intHDD/birdnet_data/bev_a2d2"
            save_camera_dirctory = os.path.join(save_dirctory, split, folder, 'camera')
            save_label_dirctory = os.path.join(save_dirctory, split, folder, 'label')

            num_files = len(camera_file_names)
            if not os.path.exists(save_label_dirctory):
                os.makedirs(save_label_dirctory)
            if not os.path.exists(save_camera_dirctory):
                os.makedirs(save_camera_dirctory)

            for i, camera_file_name in enumerate(camera_file_names):
                seq_name = camera_file_name.split('/')[-1]
                file_name = seq_name.split('.')[0]
                file_num = file_name.split('_')[-1]

                img = cv2.imread(camera_file_name)
                save_camera = os.path.join(save_camera_dirctory, f"{file_num}.png")

                cv2.imwrite(save_camera, img)

                file_name_bboxes = seq_name.replace("camera_", "label3D_").replace("png", "json")
                file_name_bboxes = os.path.join("/".join(camera_file_name.split('/')[:-3]), "label3D",
                                                "cam_front_center", file_name_bboxes)

                save_label = os.path.join(save_label_dirctory, f"{file_num}.json")
                boxes = a2.read_bounding_boxes(file_name_bboxes)
                with open(save_label, "w") as make_file:
                    json.dump(boxes, make_file, indent="\t")

                print_progress(f"-- Progress: {i}/{num_files} {j}/{num_folder}")


def print_progress(status_msg):
    # NOTE: the \r which means the line should overwrite itself.
    msg = "\r" + status_msg
    # Print it.
    sys.stdout.write(msg)
    sys.stdout.flush()


if __name__ == '__main__':
    path = '/media/dolphin/intHDD/a2d2'
    merge_to_all_image(path)
