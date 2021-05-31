#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python


import open3d as o3d
import numpy as np
import os
import glob
import pprint
import cv2

import get_transform as gt

count = 0


def load_nps():
    root_path = 'data/lidar/'
    file_names  = sorted(glob.glob(os.path.join(root_path, '*.npz')))

    count = 0
    for i, file_name_lidar  in enumerate(file_names ):
        print(file_name_lidar)
        seq_name = file_name_lidar.split('/')[2]
        print(seq_name)
        file_name_image = extract_image_file_name_from_lidar_file_name(file_name_lidar)
        file_name_image = os.path.join(root_path, seq_name, 'camera/cam_front_center/', file_name_image)
        image_front_center = cv2.imread(file_name_image)



        lidar_front_center = np.load(file_name_lidar)
        # pprint.pprint(list(lidar_front_center.keys()))
        points = lidar_front_center['pcloud_points']
        reflectance = lidar_front_center['pcloud_attr.reflectance']
        timestamps = lidar_front_center['pcloud_attr.timestamp']
        rows = lidar_front_center['pcloud_attr.row']
        cols = lidar_front_center['pcloud_attr.col']
        distance = lidar_front_center['pcloud_attr.distance']
        depth = lidar_front_center['pcloud_attr.depth']
        lidar_ids = lidar_front_center['pcloud_attr.lidar_id']

        show_lidar(lidar_front_center)
        # pcd_front_center = create_open3d_pc(lidar_front_center)
        # o3d.visualization.draw_geometries([pcd_front_center])


def show_lidar(lidar_front_center):
    config = gt.load_json()
    src_view_front_center = config["cameras"]["front_center"]["view"]
    vehicle_view = target_view = config['vehicle']['view']

    lidar_front_center = project_lidar_from_to(lidar_front_center, src_view_front_center, vehicle_view)
    pcd_front_center = create_open3d_pc(lidar_front_center)

    o3d.visualization.draw_geometries([pcd_front_center])



def colours_from_reflectances(reflectances):
    return np.stack([reflectances, reflectances, reflectances], axis=1)


def create_open3d_pc(lidar, cam_image=None):
    # create open3d point cloud
    pcd = o3d.geometry.PointCloud()

    # assign point coordinates
    pcd.points = o3d.utility.Vector3dVector(lidar['pcloud_points'])

    # assign colours
    if cam_image is None:
        median_reflectance = np.median(lidar['pcloud_attr.reflectance'])
        colours = colours_from_reflectances(lidar['pcloud_attr.reflectance']) / (median_reflectance * 5)

        # clip colours for visualisation on a white background
        colours = np.clip(colours, 0, 0.75)
    else:
        rows = (lidar['pcloud_attr.row'] + 0.5).astype(np.int)
        cols = (lidar['pcloud_attr.col'] + 0.5).astype(np.int)
        colours = cam_image[rows, cols, :] / 255.0

    pcd.colors = o3d.utility.Vector3dVector(colours)

    return pcd


def project_lidar_from_to(lidar, src_view, target_view):
    lidar = dict(lidar)
    trans = gt.transform_from_to(src_view, target_view)
    points = lidar['pcloud_points']
    points_hom = np.ones((points.shape[0], 4))
    points_hom[:, 0:3] = points
    points_trans = (np.dot(trans, points_hom.T)).T
    lidar['pcloud_points'] = points_trans[:, 0:3]

    return lidar

def extract_image_file_name_from_lidar_file_name(file_name_lidar):
    file_name_image = file_name_lidar.split('/')
    file_name_image = file_name_image[-1].split('.')[0]
    file_name_image = file_name_image.split('_')
    file_name_image = file_name_image[0] + '_' + \
                        'camera_' + \
                        file_name_image[2] + '_' + \
                        file_name_image[3] + '.png'

    return file_name_image

if __name__ == '__main__':
    nps_file_names = load_nps()
    show_lidar(nps_file_names)
