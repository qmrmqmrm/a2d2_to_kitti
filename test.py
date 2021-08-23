import numpy as np
import json
import glob, os


def load_json(root_path):
    print(root_path)
    file_names = sorted(glob.glob(os.path.join(root_path, '*.json')))
    print(file_names)
    configs =list()
    for i, file_name in enumerate(file_names):
        with open(file_name, 'r') as f:
            config = json.load(f)

        configs.append(config)
        print(config)
    return configs


if __name__ == '__main__':
    root = "/media/dolphin/intHDD/birdnet_data/bv_a2d2/annotations"
    configs = load_json(root)
    print(configs)