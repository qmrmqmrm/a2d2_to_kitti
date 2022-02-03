#!/home/dolphin/.pyenv/versions/open3d/pin/python
import numpy as np
import sys
import shutil
import math
import open3d as o3d
import numpy as np
import os
import glob
import load_and_save as sf


def print_progress(status_msg):
    # NOTE: the \r which means the line should overwrite itself.
    msg = "\r" + status_msg
    # Print it.
    sys.stdout.write(msg)
    sys.stdout.flush()


def load_kitti_velodyne(root_path):
    if root_path[-3:] == "bin":
        file_names = sorted(glob.glob(os.path.join(root_path)))
    else:
        file_names = sorted(glob.glob(os.path.join(root_path, 'bv_kitti/velodyne/*.bin')))

    velodyne = dict()
    # print(file_names)
    num_files = len(file_names)
    for i, file_name_lidar in enumerate(file_names):
        file_num = file_name_lidar.split("/")[-1]
        file_num = file_num.split(".")[0]
        with open(file_name_lidar, 'rb') as f:
            data = np.fromfile(f, np.float32)
            ss = int(data.shape[0] / 4)
            data = np.reshape(data[:ss * 4], (ss, 4))
            velodyne[file_num] = data

        print_progress(f"-- Progress: {i}/{num_files}")
    return velodyne


def make_open3d_from_kitti_velodyne(velodyne, show_view=True, save=True):
    mesh_box = o3d.geometry.TriangleMesh.create_box(width=10.0,
                                                    height=10.0,
                                                    depth=10.0)
    mesh_box.compute_vertex_normals()
    mesh_box.paint_uniform_color([0.9, 0.1, 0.1])
    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=10.0)
    mesh_sphere.compute_vertex_normals()
    mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])
    mesh_cylinder = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3,
                                                              height=10.0)
    mesh_cylinder.compute_vertex_normals()
    mesh_cylinder.paint_uniform_color([0.1, 0.9, 0.1])
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=6, origin=[-2, -2, -2])
    save_name = os.path.join(root_path, 'save_velo_2')
    print()
    print(save_name)
    count = 0
    num_files = len(velodyne.items())
    for key, value in velodyne.items():

        points = value[:, :3]

        if show_view:
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.visualization.draw_geometries([pcd, mesh_frame])

        if save:
            reflence = value[:, 3:4]
            # test_rot = create_rotation_matrix([0, -np.pi / 6, 0])
            # points_rot = np.dot(test_rot, points.T)
            velodyne = np.concatenate([points, reflence], axis=1)
            velodyne_bin = bytes(velodyne)
            # save_name = sorted(glob.glob(os.path.join(save_name, f'.bin')))
            sf.save_bin(save_name, velodyne_bin, key)
        count += 1
        print_progress(f"-- Progress: {count}/{num_files}")


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
    # root_path = '/media/dolphin/intHDD/birdnet_data/a2d2/training/velodyne/000003033.bin'
    # root_path = '/media/dolphin/intHDD/birdnet_data/make_bev_3/20181204_170238/velodyne'
    # root_path = '/media/dolphin/intHDD/birdnet_data/save_velo_2/000013.bin'
    root_path = '/media/dolphin/intHDD/birdnet_data'
    velodyne = load_kitti_velodyne(root_path)
    make_open3d_from_kitti_velodyne(velodyne, show_view=False, save=True)
