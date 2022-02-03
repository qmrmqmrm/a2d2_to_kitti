#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import os
import sys
import glob
import shutil
import math

import get_calibration_form as gc
import bounding_boxes as a2
import load_and_save as sf


def convert_a2d2_to_kitti(root_path):
    calibriation_dict = gc.get_calibration(root_path)
    folders = ['20180807_145028', '20180810_142822', '20180925_101535', '20180925_112730', '20180925_124435',
               '20180925_135056', '20181008_095521', '20181016_125231', '20181107_132300', '20181107_132730',
               '20181107_133258', '20181108_084007', '20181108_091945', '20181108_103155', '20181108_123750',
               '20181204_135952', '20181204_154421', '20181204_170238']

    for folder in folders:
        laidar_file_names = sorted(glob.glob(
            os.path.join(root_path, 'bbox/camera_lidar_semantic_bboxes', folder, 'lidar/cam_front_center/*.npz')))

        save_dirctory = "/media/dolphin/intHDD/birdnet_data/make_bev_3"
        # save_label_txt_dirctory = os.path.join(save_dirctory, folder, 'label')
        # save_lists_dirctory = os.path.join(save_dirctory, folder, 'lists')
        save_lidar_dirctory = os.path.join(save_dirctory, folder, "velodyne")
        save_calib_dirctory = os.path.join(save_dirctory, folder, 'calib')
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
            # file_name_bboxes = seq_name.replace("lidar_", "label3D_").replace(".npz", ".json")
            #
            # file_name_bboxes = os.path.join("/".join(lidar_file_name.split('/')[:-3]), "label3D", "cam_front_center",
            #                                 file_name_bboxes)
            # print(file_name_bboxes)
            # boxes = a2.read_bounding_boxes(file_name_bboxes)
            # lines = a2.convert_a2d2_to_kitti_label(boxes)

            # sf.save_txt(save_label_txt_dirctory, lines, file_num)
            sf.save_bin(save_lidar_dirctory, velodyne_bin, file_num)
            sf.save_txt_dict(save_calib_dirctory, calibriation_dict, file_num)
            print_progress(f"-- Progress: {i}/{num_files}")

        # val_len = int(len(num_list) * 0.2)
        # val_list = num_list[:val_len]
        # train_list = num_list[val_len:]
        #
        # sf.save_txt(save_lists_dirctory, num_list, "trainval")
        # sf.save_txt(save_lists_dirctory, val_list, "valsplit_chen")
        # sf.save_txt(save_lists_dirctory, train_list, "trainsplit_chen")


def get_pcloud(npz_file_name):
    lidar_front_center = np.load(npz_file_name)
    points = lidar_front_center['points']
    reflectance = lidar_front_center['reflectance']
    test_rot = create_rotation_matrix([0,-np.pi/6,0])
    points_rot = np.dot(test_rot, points.T)
    reflectance = np.reshape(reflectance, (reflectance.shape[0], 1))
    velodyne = np.concatenate([points_rot.T, reflectance], axis=1)

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

# rotation matrix 생성
def create_rotation_matrix(euler):
    (yaw, pitch, roll) = euler

    yaw_matrix = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]
    ])

    pitch_matrix = np.array([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]
    ])

    roll_matrix = np.array([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]
    ])

    rotation_matrix_a = np.dot(pitch_matrix, roll_matrix)
    rotation_matrix = np.dot(yaw_matrix, rotation_matrix_a)

    return rotation_matrix


if __name__ == '__main__':
    root_path = '/media/dolphin/intHDD/a2d2'
    convert_a2d2_to_kitti(root_path)
