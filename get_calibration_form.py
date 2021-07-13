#!/home/ri-1080/.pyenv/versions/ros_py36/pin/python

import numpy as np
import os
import glob
import json
import pprint

EPSILON = 1.0e-10


def load_json(root_path):
    file_names = sorted(glob.glob(os.path.join(root_path, '*.json')))

    # print(file_names)
    for i, file_name in enumerate(file_names):
        with open(file_name, 'r') as f:
            config = json.load(f)

    return config


def get_origin_of_a_view(view):
    return view['origin']


def get_axes_of_a_view(view):
    x_axis = view['x-axis']
    y_axis = view['y-axis']

    x_axis_norm = np.linalg.norm(x_axis)
    y_axis_norm = np.linalg.norm(y_axis)

    if (x_axis_norm < EPSILON or y_axis_norm < EPSILON):
        raise ValueError("Norm of input vector(s) too small.")

    # normalize the axes
    x_axis = x_axis / x_axis_norm
    y_axis = y_axis / y_axis_norm

    # make a new y-axis which lies in the original x-y plane, but is orthogonal to x-axis
    y_axis = y_axis - x_axis * np.dot(y_axis, x_axis)

    # create orthogonal z-axis
    z_axis = np.cross(x_axis, y_axis)

    # calculate and check y-axis and z-axis norms
    y_axis_norm = np.linalg.norm(y_axis)
    z_axis_norm = np.linalg.norm(z_axis)

    if (y_axis_norm < EPSILON) or (z_axis_norm < EPSILON):
        raise ValueError("Norm of view axis vector(s) too small.")

    # make x/y/z-axes orthonormal
    y_axis = y_axis / y_axis_norm
    z_axis = z_axis / z_axis_norm

    return x_axis, y_axis, z_axis


def get_transform_to_global(view):
    # get axes
    x_axis, y_axis, z_axis = get_axes_of_a_view(view)

    # get origin
    origin = get_origin_of_a_view(view)
    transform_to_global = np.eye(4)

    # rotation
    transform_to_global[0:3, 0] = x_axis
    transform_to_global[0:3, 1] = y_axis
    transform_to_global[0:3, 2] = z_axis

    # origin
    transform_to_global[0:3, 3] = origin

    return transform_to_global


def get_transform_from_global(view):
    # get transform to global
    transform_to_global = get_transform_to_global(view)
    trans = np.eye(4)
    rot = np.transpose(transform_to_global[0:3, 0:3])
    trans[0:3, 0:3] = rot
    trans[0:3, 3] = np.dot(rot, -transform_to_global[0:3, 3])

    return trans


def get_rot_from_global(view):
    # get transform to global
    transform_to_global = get_transform_to_global(view)
    # get rotation
    rot = np.transpose(transform_to_global[0:3, 0:3])

    return rot


def get_rot_to_global(view):
    # get transform to global
    transform_to_global = get_transform_to_global(view)
    # get rotation
    rot = transform_to_global[0:3, 0:3]

    return rot


def rot_from_to(src, target):  # target -> src
    rot = np.dot(get_rot_from_global(target), get_rot_to_global(src))

    return rot


def transform_from_to(src, target):
    transform = np.dot(get_transform_from_global(target), get_transform_to_global(src))

    return transform


def get_calibration(root_path):
    config = load_json(root_path)
    cam_matrix = config['cameras']['front_center']['CamMatrix']

    target_view = config['cameras']['front_center']['view']
    camera_transform = get_transform_to_global(target_view)
    src_view = config['lidars']['front_center']['view']
    rot = rot_from_to(src_view, target_view)
    transform = transform_from_to(src_view, target_view)

    ZERO = "0.000000000000e+00"
    calibriation_dict = dict()
    print(cam_matrix)
    cam_matrix = np.array(cam_matrix).reshape(3, 3)
    print(cam_matrix)
    one = np.eye(3)
    zero = np.zeros([3, 1])
    matrix34 = np.concatenate((one, zero), axis=1)
    cam_matrix = cam_matrix @ matrix34
    print(cam_matrix)
    cam_matrix = (np.reshape(cam_matrix, (-1)).astype(np.str)).tolist()
    print(len(cam_matrix))
    transform = np.reshape(transform, (-1)).astype(np.str)
    rot = np.reshape(rot, (-1)).astype(np.str)

    calibriation_dict["P0"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["P1"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["P2"] = " ".join(cam_matrix[:12])
    calibriation_dict["P3"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["R0_rect"] = " ".join(rot)
    calibriation_dict["Tr_velo_to_cam"] = " ".join(transform[:12])
    return calibriation_dict


if __name__ == '__main__':
    root_path = '/media/ri-1080/IanBook12T/datasets/raw_zips/a2d2'
    a = get_calibration(root_path)
