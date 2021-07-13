import os


def save_bin(save_dirctory, data,file_name):
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


def save_txt_dict(save_dirctory, dict ,file_name):
    if not os.path.exists(save_dirctory):
        os.makedirs(save_dirctory)
    save_txt_file_name = os.path.join(save_dirctory, f'{file_name}.txt')

    if not os.path.exists(save_txt_file_name):
        with open(save_txt_file_name, "w") as f:
            for catagoly, value in dict.items():
                data = f"{catagoly}: {value}\n"
                f.write(data)
