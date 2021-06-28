import numpy as np
import json


def read_bounding_boxes(file_name_bboxes):
    # open the file
    with open(file_name_bboxes, 'r') as f:
        bboxes = json.load(f)

    boxes = []  # a list for containing bounding boxes

    for bbox in bboxes.keys():
        bbox_read = {}  # a dictionary for a given bounding box
        bbox_read['class'] = bboxes[bbox]['class']
        bbox_read['truncation'] = bboxes[bbox]['truncation']
        bbox_read['occlusion'] = int(bboxes[bbox]['occlusion'])
        bbox_read['alpha'] = bboxes[bbox]['alpha']
        bbox_read['top'] = bboxes[bbox]['2d_bbox'][0]
        bbox_read['left'] = bboxes[bbox]['2d_bbox'][1]
        bbox_read['bottom'] = bboxes[bbox]['2d_bbox'][2]
        bbox_read['right'] = bboxes[bbox]['2d_bbox'][3]
        bbox_read['center'] = np.array(bboxes[bbox]['center'])
        bbox_read['size'] = np.array(bboxes[bbox]['size'])
        angle = bboxes[bbox]['rot_angle']
        bbox_read['rot_angle'] = angle
        axis = np.array(bboxes[bbox]['axis'])
        bbox_read['rotation'] = axis_angle_to_rotation_mat(axis, angle)
        boxes.append(bbox_read)

    return boxes


def axis_angle_to_rotation_mat(axis, angle):
    return np.cos(angle) * np.eye(3) + \
           np.sin(angle) * skew_sym_matrix(axis) + \
           (1 - np.cos(angle)) * np.outer(axis, axis)


def skew_sym_matrix(u):
    return np.array([[0, -u[2], u[1]],
                     [u[2], 0, -u[0]],
                     [-u[1], u[0], 0]])


def convert_a2d2_to_kitti_label(boxes):
    '''
    ['type', 'truncated', 'occluded', 'alpha', 'bbox_xmin', 'bbox_ymin',
    'bbox_xmax', 'bbox_ymax', 'dimensions_1', 'dimensions_2', 'dimensions_3',
    'location_1', 'location_2', 'location_3', 'rotation_y']
    '''
    lines = list()
    for i, bbox_read in enumerate(boxes):
        line = f"{bbox_read['class']} {bbox_read['truncation']:.2f} {bbox_read['occlusion']} {bbox_read['alpha']:.2f} {bbox_read['left']:.2f} {bbox_read['top']:.2f} {bbox_read['right']:.2f} {bbox_read['bottom']:.2f} {bbox_read['size'][0]:.2f} {bbox_read['size'][1]:.2f} {bbox_read['size'][2]:.2f} {bbox_read['center'][0]:.2f} {bbox_read['center'][1]:.2f} {bbox_read['center'][2]:.2f} {bbox_read['rot_angle']:.2f}"
        lines.append(line)
    return lines
