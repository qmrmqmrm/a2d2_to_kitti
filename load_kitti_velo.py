#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python

import open3d as o3d
import numpy as np
import os
import glob


def load_kitti_velodyne():
    root_path = 'data/velodyne/'
    file_names = sorted(glob.glob(os.path.join(root_path, '*.bin')))

    velodyne = dict()
    for i, file_name_lidar in enumerate(file_names):
        file_numes = file_name_lidar.split("/")[-1]
        file_numes = file_numes.split(".")[0]
        with open(file_name_lidar, 'rb') as f:
            data = np.fromfile(f, np.float32)
            ss = int(data.shape[0] / 4)
            data = np.reshape(data[:ss * 4], (ss, 4))
            velodyne[file_numes] = data
    return velodyne


def make_open3d_from_kitti_velodyne(velodyne, show_view=True):
    for key, value in velodyne.items():
        pcd = o3d.geometry.PointCloud()
        points = value[:, :3]
        print(points.shape)

        pcd.points = o3d.utility.Vector3dVector(points)
        if show_view:
            o3d.visualization.draw_geometries([pcd])


if __name__ == '__main__':
    velodyne = load_kitti_velodyne()
    make_open3d_from_kitti_velodyne(velodyne)
