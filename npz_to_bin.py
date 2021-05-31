#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python
import numpy as np
import os
import glob


def load_a2d2_npz():
    root_path = 'data/'
    file_names = sorted(glob.glob(os.path.join(root_path, 'lidar/*.npz')))

    for i, file_name_lidar in enumerate(file_names):
        # print(file_name_lidar)
        seq_name = file_name_lidar.split('/')[2]
        file_name = seq_name.split('.')[0]
        save_bin_file_name = os.path.join(root_path, 'lidar_bin/', file_name + '.bin')

        lidar_front_center = np.load(file_name_lidar)
        points = lidar_front_center['pcloud_points']
        reflectance = lidar_front_center['pcloud_attr.reflectance']

        reflectance = np.reshape(reflectance, (reflectance.shape[0], 1))
        velodyne = np.concatenate([points, reflectance], axis=1)
        velodyne_bin = np.reshape(velodyne, (-1)).astype(np.float32)
        velodyne_bin = bytes(velodyne_bin)

        with open(save_bin_file_name, 'wb') as f:
            f.write(velodyne_bin)


if __name__ == '__main__':
    nps_file_names = load_a2d2_npz()
