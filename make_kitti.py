#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python
import numpy as np
import os
import glob

import get_transform as gt
import a2d2_tutorial as a2


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


def convert_a2d2_to_kitti(root_path, dataset):
    file_names = sorted(
        glob.glob(os.path.join(root_path, 'bbox/camera_lidar_semantic_bboxes/*/lidar/cam_front_center/*.npz')))
    save_dirctory = "/home/ri-1080/work2/a2d2_to_kitti/data/training"
    num_list = list()
    for i, file_name_lidar in enumerate(file_names):
        seq_name = file_name_lidar.split('/')[-1]
        file_name = seq_name.split('.')[0]
        file_num = file_name.split('_')[-1]

        velodyne = get_pcloud(file_name_lidar)
        velodyne_bin = np.reshape(velodyne, (-1)).astype(np.float32)
        velodyne_bin = bytes(velodyne_bin)

        file_name_bboxes = extract_bboxes_file_name_from_image_file_name(file_name_lidar)
        file_name_bboxes = os.path.join("/".join(file_name_lidar.split('/')[:-3]), 'label3D/cam_front_center',
                                        file_name_bboxes)
        boxes = a2.read_bounding_boxes(file_name_bboxes)
        lines = a2.convert_a2d2_to_kitti_label(boxes)

        calibriation_dict = gt.save_txt_calib(root_path)

        save_label_txt(save_dirctory, file_num, lines)
        save_lider_bin(save_dirctory, file_num, velodyne_bin)
        save_calib_txt(save_dirctory, file_num, calibriation_dict)
        num_list.append(file_num)
    save_list_txt(save_dirctory,num_list,"trainval")
    num_list_len  = len(num_list)
    val_len = int(num_list_len*0.2)
    val_list = num_list[:val_len]
    train_list = num_list[val_len:]
    save_list_txt(save_dirctory,val_list,"valsplit_chen")
    save_list_txt(save_dirctory,train_list,"trainsplit_chen")






def save_lider_bin(save_dirctory, file_num, velodyne_bin):
    save_lidar_dirctory = os.path.join(save_dirctory, "velodyne")
    if not os.path.exists(save_lidar_dirctory):
        os.makedirs(save_lidar_dirctory)
    save_bin_file_name = os.path.join(save_lidar_dirctory, file_num + '.bin')

    if not os.path.exists(save_bin_file_name):
        with open(save_bin_file_name, 'wb') as f:
            f.write(velodyne_bin)
            f.close()


def save_label_txt(save_dirctory, file_num, calibriation_dict):
    save_txt_dirctory = os.path.join(save_dirctory, 'label')
    if not os.path.exists(save_txt_dirctory):
        os.makedirs(save_txt_dirctory)
    save_txt_file_name = os.path.join(save_txt_dirctory, file_num + '.txt')

    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for line in calibriation_dict:
                data = f"{line}\n"
                f.write(data)


def save_calib_txt(save_dirctory, file_num, calibriation_dict):
    save_txt_dirctory = os.path.join(save_dirctory, 'calib')
    if not os.path.exists(save_txt_dirctory):
        os.makedirs(save_txt_dirctory)
    save_txt_file_name = os.path.join(save_txt_dirctory, file_num + '.txt')

    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for catagoly, value in calibriation_dict.items():
                data = f"{catagoly}: {value}\n"
                f.write(data)


def save_list_txt(save_dirctory, num_list , file_name):
    save_txt_dirctory = os.path.join(save_dirctory, 'lists')
    if not os.path.exists(save_txt_dirctory):
        os.makedirs(save_txt_dirctory)
    save_txt_file_name = os.path.join(save_txt_dirctory, f'{file_name}.txt')

    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for line in num_list:
                data = f"{line}\n"
                f.write(data)


if __name__ == '__main__':
    root_path = '/media/ri-1080/IanBook12T/datasets/raw_zips/a2d2'
    dataset = 'a2d2'
    convert_a2d2_to_kitti(root_path, dataset)
