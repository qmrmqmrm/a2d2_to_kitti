#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python

import get_transform as gt
import numpy as np


def project_lidar_from_to(lidar, src_view, target_view):
    lidar = dict(lidar)
    trans = gt.transform_from_to(src_view, target_view)
    points = lidar['points']
    points_hom = np.ones((points.shape[0], 4))
    points_hom[:, 0:3] = points
    points_trans = (np.dot(trans, points_hom.T)).T
    lidar['points'] = points_trans[:, 0:3]

    return lidar


if __name__ == '__main__':
    project_lidar_from_to()