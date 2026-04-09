import Image_Reconstruction as ir
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.colors import hsv_to_rgb
import imagej
from tqdm import tqdm

list1 = [(244,253),(254,263),(264,273),(274,283),(284,293)]

range1 = [180, 200]
range2 = [224,394]
range3 = [220,300]

file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\37data.dat'

data = ir.Reconstruction532(file_path)

#bscan = di.Bscan(data, range1)
#map = di.Map(data)
#slice = di.Slice(data, range2)
#P_map = di.Partial_Map(data, range3)

print("a")
ij = imagej.init('D:/software/fiji-latest-win64-jdk/Fiji', mode='interactive')
save_dir = "Output"
cwd = os.getcwd()
save_dir = os.path.join(cwd, save_dir)
os.makedirs(save_dir, exist_ok=True)
print(os.path.join(save_dir))

for rangeN in list1:
    P_map = ir.Partial_Map(data, rangeN)

    plt.figure(figsize=(4,10))
    plt.axis('off')
    plt.imshow(P_map, cmap='hot', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"P_Map_{rangeN[0]}.tif"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()

files = ir.get_path([save_dir])
print(files)

for file in tqdm(files):
    ir.Skeletonization(file, ij)



'''
for i, b in enumerate(bscan):

    plt.figure(figsize=(4,12))
    plt.axis('off')
    plt.imshow(b, cmap='gray', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"bscan_{i:03d}.tif"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()

plt.figure(figsize=(4,10))
plt.imshow(map, cmap='hot', aspect='auto')

plt.savefig(os.path.join(save_dir, f"P_Map.tif"),
            dpi=300,
            bbox_inches='tight',
            pad_inches=0)

plt.close()

for i, s in enumerate(slice):

    plt.figure(figsize=(4,10))
    plt.axis('off')
    plt.imshow(s, cmap='gray', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"slice_{i+range2[0]:03d}.tif"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()

s = np.ones_like(h)   # 饱和度固定为1（颜色鲜艳）

# 组合 HSV
hsv = np.stack([h, s, v], axis=-1)

# 转 RGB
rgb = hsv_to_rgb(hsv)

plt.figure(figsize=(4,10))
plt.axis('off')
plt.imshow(rgb, aspect='auto')
plt.savefig(os.path.join(save_dir, f"D_Map.png"),
            dpi=300,
            bbox_inches='tight',
            pad_inches=0)
'''