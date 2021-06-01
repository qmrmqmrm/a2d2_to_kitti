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


def save_txt_calib(root_path):
    config = load_json(root_path)
    cam_matrix = config['cameras']['front_center']['CamMatrix']
    view = config['cameras']['front_center']['view']
    transform = get_transform_from_global(view)
    rot = get_rot_from_global(view)

    ZERO = "0.000000000000e+00"
    catagolies = ["P0", "P1", "P2", "P3", "R0_rect", "Tr_velo_to_cam"]
    calibriation_dict = dict()
    cam_matrix = np.array(cam_matrix).reshape(3, 3)
    one = np.eye(3)
    zero = np.zeros([3, 1])
    matrix34 = np.concatenate((one, zero), axis=1)
    cam_matrix = cam_matrix @ matrix34 @ transform
    cam_matrix = np.reshape(cam_matrix,(-1)).astype(np.float32)
    transform = np.reshape(transform,(-1)).astype(np.float32)
    rot = np.reshape(rot,(-1)).astype(np.float32)

    calibriation_dict["P0"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["P1"] = f"{cam_matrix[0]} {cam_matrix[1]} {cam_matrix[2]} {cam_matrix[3]} {cam_matrix[4]} {cam_matrix[5]} {cam_matrix[6]} {cam_matrix[7]} {cam_matrix[8]} {cam_matrix[9]} {cam_matrix[10]} {cam_matrix[11]}"
    calibriation_dict["P2"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["P3"] = f"{ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO} {ZERO}"
    calibriation_dict["R0_rect"] = f"{rot[0]} {rot[1]} {rot[2]} {rot[3]} {rot[4]} {rot[5]} {rot[6]} {rot[7]} {rot[8]}"
    calibriation_dict["Tr_velo_to_cam"] = f"{transform[0]} {transform[1]} {transform[2]} {transform[3]} {transform[4]} {transform[5]} {transform[6]} {transform[7]} {transform[8]} {transform[9]} {transform[10]} {transform[11]}"

    return calibriation_dict
