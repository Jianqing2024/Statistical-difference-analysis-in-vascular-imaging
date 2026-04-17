import os
from glob import glob
from .Basic_computation import *
import numpy as np

def get_path(folders):
    # 给定一个列表，其中存放所有需要查找的文件夹
    # 用于存放所有文件的列表
    current_dir = os.getcwd()
    all_files = []

    for folder in folders:
        folder_path = os.path.join(current_dir, folder)
        if os.path.exists(folder_path):
            # 查找该文件夹下所有 .tif 文件
            png_files = glob(os.path.join(folder_path, '*.tif'))
            all_files.extend(png_files)  # 添加到总列表
        else:
            print(f"警告: 文件夹不存在 -> {folder_path}")
    return all_files

def split_range(start, end, step=2):
    groups = []
    for i in range(start, end + 1, step):
        s = i
        e = min(i + step - 1, end)

        # 只保留首尾不同的区间
        if s != e:
            groups.append([s, e])

    return groups

def Split_into_two(file, save_path):
    data = Reconstruction532(file)

    data1 = data[0:750,:,:]
    data2 = data[750:1500,:,:]

    filename = os.path.splitext(os.path.basename(file))[0]

    save_path1 = os.path.join(save_path, f'{filename}1.npy')
    save_path2 = os.path.join(save_path, f'{filename}2.npy')

    np.save(save_path1, data1)
    np.save(save_path2, data2)

    return save_path1, save_path2