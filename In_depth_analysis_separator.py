import Image_Reconstruction as ir
import os
from glob import glob

current_dir = os.getcwd()
all_files = []

folder_path = os.path.join(current_dir, 'Installments')

if os.path.exists(folder_path):
    # 查找该文件夹下所有指定格式文件
    png_files = glob(os.path.join(folder_path, '*.dat'))
    all_files.extend(png_files)  # 添加到总列表
else:
    print(f"警告: 文件夹不存在 -> {folder_path}")

Temporary_path = os.path.join(current_dir, 'Installments', 'data')
os.makedirs(Temporary_path, exist_ok=True)

for file in all_files:
    ir.Split_into_two(file, Temporary_path)