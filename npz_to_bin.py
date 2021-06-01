#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python
import numpy as np
import os
import glob

import get_transform as gt


def load_a2d2_npz(root_path):
    file_names = sorted(glob.glob(os.path.join(root_path, 'lidar/*.npz')))
    for i, file_name_lidar in enumerate(file_names):
        seq_name = file_name_lidar.split('/')[2]
        file_name = seq_name.split('.')[0]
        file_num= file_name.split('_')[-1][-7:-1]
        print(file_num)

        lidar_front_center = np.load(file_name_lidar)
        save_bin_dirctory = os.path.join(root_path, 'lidar_bin')
        if not os.path.exists(save_bin_dirctory):
            os.makedirs(save_bin_dirctory)
        save_bin_file_name = os.path.join(save_bin_dirctory, file_num + '.bin')


        save_txt_dirctory = os.path.join(root_path, 'calib_txt')
        print(save_txt_dirctory)
        if not os.path.exists(save_txt_dirctory):
            os.makedirs(save_txt_dirctory)
        save_txt_file_name = os.path.join(save_txt_dirctory, file_num + '.txt')


        points = lidar_front_center['pcloud_points']
        reflectance = lidar_front_center['pcloud_attr.reflectance']

        reflectance = np.reshape(reflectance, (reflectance.shape[0], 1))
        velodyne = np.concatenate([points, reflectance], axis=1)
        velodyne_bin = np.reshape(velodyne, (-1)).astype(np.float32)
        velodyne_bin = bytes(velodyne_bin)
        if not os.path.exists(save_bin_file_name):
            with open(save_bin_file_name, 'wb') as f:
                f.write(velodyne_bin)
                f.close()
        calibriation_dict = gt.save_txt_calib(root_path)
        if not os.path.exists(save_txt_file_name):

            with open(save_txt_file_name, "w") as f:
                for catagoly, value in calibriation_dict.items():
                    data = f"{catagoly}: {value}\n"

                    f.write(data)


if __name__ == '__main__':
    root_path = 'data/'
    load_a2d2_npz(root_path)
