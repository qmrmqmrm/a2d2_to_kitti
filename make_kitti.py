#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import shutil

import get_calibration_form as gc
import bounding_boxes as a2
import load_and_save as sf

def convert_a2d2_to_kitti(root_path):
    calibriation_dict = gc.get_calibration(root_path)
    laidar_file_names = sorted(
        glob.glob(os.path.join(root_path, 'bbox/camera_lidar_semantic_bboxes/*/lidar/cam_front_center/*.npz')))

    save_dirctory = "/home/dolphin/work/a2d2_to_kitti/data/training"
    save_label_txt_dirctory = os.path.join(save_dirctory, 'label')
    save_lists_dirctory = os.path.join(save_dirctory, 'lists')
    save_lidar_dirctory = os.path.join(save_dirctory, "velodyne")
    save_calib_dirctory = os.path.join(save_dirctory, 'calib')
    num_list = list()
    num_files = len(laidar_file_names)

    for i, lidar_file_name in enumerate(laidar_file_names):
        seq_name = lidar_file_name.split('/')[-1]
        file_name = seq_name.split('.')[0]
        file_num = file_name.split('_')[-1]
        num_list.append(file_num)


        velodyne = get_pcloud(lidar_file_name)
        velodyne_bin = np.reshape(velodyne, (-1)).astype(np.float32)
        velodyne_bin = bytes(velodyne_bin)

        # file_name_bboxes = extract_bboxes_file_name_from_image_file_name(lidar_file_name)
        file_name_bboxes = seq_name.replace("lidar","label3D").replace("npz","json")
        file_name_bboxes = os.path.join("/".join(lidar_file_name.split('/')[:-3]), "label3D", "cam_front_center",
                                        file_name_bboxes)
        boxes = a2.read_bounding_boxes(file_name_bboxes)
        lines = a2.convert_a2d2_to_kitti_label(boxes)

        sf.save_txt(save_label_txt_dirctory, lines, file_num)
        sf.save_bin(save_lidar_dirctory, velodyne_bin, file_num)
        sf.save_txt_dict(save_calib_dirctory, calibriation_dict, file_num)
        print_progress(f"-- Progress: {i}/{num_files}")

    val_len = int(len(num_list) * 0.2)
    val_list = num_list[:val_len]
    train_list = num_list[val_len:]

    sf.save_txt(save_lists_dirctory, num_list, "trainval")
    sf.save_txt(save_lists_dirctory, val_list, "valsplit_chen")
    sf.save_txt(save_lists_dirctory, train_list, "trainsplit_chen")


def get_pcloud(npz_file_name):
    lidar_front_center = np.load(npz_file_name)
    points = lidar_front_center['points']
    reflectance = lidar_front_center['reflectance']
    reflectance = np.reshape(reflectance, (reflectance.shape[0], 1))
    velodyne = np.concatenate([points, reflectance], axis=1)

    return velodyne


def extract_bboxes_file_name_from_image_file_name(file_name_image):
    file_name_bboxes = file_name_image.split('/')
    file_name_bboxes = file_name_bboxes[-1].split('.')[0]
    file_name_bboxes = file_name_bboxes.split('_')
    file_name_bboxes = file_name_bboxes[0] + '_' + \
                       'label3D_' + \
                       file_name_bboxes[2] + '_' + \
                       file_name_bboxes[3] + '.json'

    return file_name_bboxes


def print_progress(status_msg):
    # NOTE: the \r which means the line should overwrite itself.
    msg = "\r" + status_msg
    # Print it.
    sys.stdout.write(msg)
    sys.stdout.flush()


if __name__ == '__main__':
    root_path = '/media/dolphin/intHDD/a2d2'
    convert_a2d2_to_kitti(root_path)
