import numpy as np


# rotation matrix 생성
def create_rotation_matrix(euler):
    (yaw, pitch, roll) = euler

    yaw_matrix = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    pitch_matrix = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    roll_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    rotation_matrix_a = np.dot(pitch_matrix, roll_matrix)
    rotation_matrix = np.dot(yaw_matrix, rotation_matrix_a)

    return rotation_matrix


# transformation matrix 생성
def make_transformation_matrix(r_matrix, t_matrix):
    matrix_3x4 = np.concatenate((r_matrix, t_matrix), axis=1)
    zero_one = np.array([[0., 0., 0., 1.]])
    matrix_4x4 = np.concatenate((matrix_3x4, zero_one), axis=0)
    return matrix_4x4

# transformation matrix 에서 quaternion 과 translation 추출
def get_rpt_to_rotation_vector(matrix):
    print(matrix)
    r_11 = matrix[0, 0]  # cos(yaw)cos(pitch)
    r_21 = matrix[1, 0]  # sin(yaw)cos(pitch)
    r_31 = matrix[2, 0]  # -sin(pitch)
    r_32 = matrix[2, 1]  # cos(pitch)sin(roll)
    r_33 = matrix[2, 2]  # cos(pitch)cos(roll)
    translation = list(matrix[:3, 3])
    yaw = np.arctan2(r_21, r_11)
    pitch = np.arctan2(-r_31, np.sqrt((np.square(r_32)) + np.square(r_33)))
    roll = np.arctan2(r_32, r_33)
    euler_deg = [180 * (yaw / np.pi), 180 * (pitch / np.pi), 180 * (roll / np.pi)]

    return translation, euler_deg

rot = create_rotation_matrix([np.pi / 2,  -np.pi / 2,0])
trans = np.zeros([3,1])
print(trans)
transformation = make_transformation_matrix(rot, trans)
print(transformation)
P2 = [1687.3369140625, 0.0, 965.4341405582381, 0.0, 0.0, 1783.428466796875, 684.4193604186803, 0.0, 0.0, 0.0, 1.0, 0.0]

Tr_velo_to_cam = [-0.029164907783669945, 0.9813154159121007, 0.19018270859158296, 0.006485201997974865,
                  -0.9990303889079639, -0.022338970750600973, -0.037937480467295066, -0.004356497977721564,
                  -0.032980148458923414, -0.19110474844719247, 0.9810154356219696, 0.1769760382952521]


a = np.array(Tr_velo_to_cam)
a = a.reshape((3, 4))
t , r = get_rpt_to_rotation_vector(a)
print("ddd")
print(t,r)
b = np.array(P2)
b = b.reshape((3, 4))
print(a)
print(b)
