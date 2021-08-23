import glob, json, os
import numpy as np


def save_bin(save_dirctory, data, file_name):
    if not os.path.exists(save_dirctory):
        os.makedirs(save_dirctory)
    save_bin_file_name = os.path.join(save_dirctory, f'{file_name}.bin')

    if not os.path.exists(save_bin_file_name):
        with open(save_bin_file_name, 'wb') as f:
            f.write(data)
            f.close()


def save_txt(save_dirctory, lines, file_name):
    if not os.path.exists(save_dirctory):
        os.makedirs(save_dirctory)
    save_txt_file_name = os.path.join(save_dirctory, f'{file_name}.txt')
    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for line in lines:
                data = f"{line}\n"
                f.write(data)


def save_txt_dict(save_dirctory, dict, file_name):
    if not os.path.exists(save_dirctory):
        os.makedirs(save_dirctory)
    save_txt_file_name = os.path.join(save_dirctory, f'{file_name}.txt')

    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for catagoly, value in dict.items():
                data = f"{catagoly}: {value}\n"
                f.write(data)


def load_json(path):
    file_names = sorted(glob.glob(os.path.join(path, '*.json')))
    assert file_names
    configs = list()
    for i, file_name in enumerate(file_names):
        with open(file_name, 'r') as f:
            config = json.load(f)
        configs.append(config)
    return configs

def load_txt(path):
    if path[-3:] == "txt":
        file_names = sorted(glob.glob(os.path.join(path)))
    else:
        file_names = sorted(glob.glob(os.path.join(path, '*.txt')))
    for i, file_name in enumerate(file_names):
        with open(file_name,"r") as f:
            label = f.read().splitlines()

            pre_objs = np.genfromtxt(label, delimiter=' ',
                                     names=['type', 'truncated', 'occluded', 'alpha', 'bbox_xmin', 'bbox_ymin',
                                            'bbox_xmax', 'bbox_ymax', 'dimensions_1', 'dimensions_2',
                                            'dimensions_3', 'location_1', 'location_2', 'location_3', 'rotation_y'],
                                            dtype=None)
    return pre_objs

if __name__ == '__main__':
    path = "/media/dolphin/intHDD/birdnet_data/bv_a2d2/"
    a =load_txt(path)