import Image_Reconstruction as ir
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from glob import glob
import numpy as np 

range1 = [210, 310]

current_dir = os.getcwd()

Temporary_path = os.path.join(current_dir, 'Installments', 'data')
os.makedirs(Temporary_path, exist_ok=True)

all_files = []
if os.path.exists(Temporary_path):
    # 查找该文件夹下所有指定格式文件
    png_files = glob(os.path.join(Temporary_path, '*.npy'))
    all_files.extend(png_files)  # 添加到总列表
else:
    print(f"警告: 文件夹不存在 -> {Temporary_path}")

for file in tqdm(all_files):
#file = "D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Installments\\data\\14data1.npy"

    data = np.load(file)

    pmap = ir.Partial_Map(data, range1, 3)

    filename = os.path.splitext(os.path.basename(file))[0]

    cwd = os.getcwd()
    save_dir = os.path.join(cwd, "Output", 'pmap', filename)
    os.makedirs(save_dir, exist_ok=True)

    for i, s in enumerate(pmap):
        plt.figure(figsize=(4,5))
        plt.axis('off')

        plt.imshow(s, cmap='gist_heat', aspect='auto')
        plt.savefig(os.path.join(save_dir, f"pmap_{i+range1[0]:03d}.tif"),
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)

        plt.close()