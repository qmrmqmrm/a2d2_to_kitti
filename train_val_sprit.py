import os
import glob
import shutil

#
# filename = 'test.txt'
# src = '/home/banana/'
# dir = '/home/banana/txt/'
# shutil.move(src + filename, dir + filename)
def load_txt(path):
    file_name = os.path.join(path)
    with open(file_name, "r") as f:
        list = f.read().splitlines()
    print(len(list))
    return list


def sprit_data(sprit,path,lists,dd):
    for list in lists:
        filename = list + dd
        src = os.path.join(path,filename)
        dir =os.path.join(path,sprit,filename)
        if not os.path.exists(dir):
            os.makedirs(dir)
        print(filename,src,dir)
        shutil.move(src, dir)

def load_data(path,list,sprit):
    camera_path = os.path.join(path,'camera')
    image_path = os.path.join(path,'image')
    label_path = os.path.join(path,'label')
    sprit_data(sprit,camera_path,list,'.png')
    sprit_data(sprit,image_path,list,'.png')
    sprit_data(sprit,label_path,list,'.json')



if __name__ == '__main__':
    path  = '/media/dolphin/intHDD/birdnet_data/my_a2d2'
    tv_list = load_txt(f'{path}/lists/trainval.txt')
    t_list = load_txt(f'{path}/lists/trainsplit_chen.txt')
    v_list = load_txt(f'{path}/lists/valsplit_chen.txt')
    load_data(path,t_list,'train')
    load_data(path,v_list,'val')
