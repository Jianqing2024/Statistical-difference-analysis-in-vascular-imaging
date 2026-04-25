import Image_Reconstruction as ir
import os
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import tifffile as tiff

cmap_data = np.loadtxt('my_cmap.txt', delimiter=',')
my_cmap = ListedColormap(cmap_data)

file = "D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Installments\\暂存\\1_1170data.dat"
data = ir.Reconstruction532(file)

range1 = [195, 320]

current_dir = os.getcwd()

slice = ir.Slice(data, range1)

filename = os.path.splitext(os.path.basename(file))[0]

cwd = os.getcwd()
save_dir = os.path.join(cwd, "Output", 'slice', filename)
os.makedirs(save_dir, exist_ok=True)

for i, s in enumerate(slice):
    plt.figure(figsize=(4,10), dpi=300)
    plt.axis('off')

    plt.imshow(s, cmap=my_cmap, aspect='auto')
    plt.savefig(os.path.join(save_dir, f"{i}.tif"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()

"""    img = tiff.imread(os.path.join(save_dir, f"{i}.tif"))

    H, W = img.shape[:2]

    # ===== 输入参数 =====
    x0 = 460   # 左下角 x（列）
    y0 = 1155   # 左下角 y（注意：这是“从下往上”）
    w = 400
    h = 400

    # ===== 坐标转换（关键）=====
    # 图像是左上角为原点，所以要转换 y
    y_top = H - y0 - h
    y_bottom = H - y0

    # ===== 裁剪 =====
    crop = img[y_top:y_bottom, x0:x0+w]

    # ===== 保存 =====
    tiff.imwrite(os.path.join(save_dir, f"{i}.tif"), crop)"""

pmap = ir.Partial_Map(data, range1, 100)

plt.figure(figsize=(4,10), dpi=300)
plt.axis('off')

plt.imshow(pmap[0], cmap='gray', aspect='auto')
plt.savefig(os.path.join(save_dir, "pmap.tif"),
            dpi=300,
            bbox_inches='tight',
            pad_inches=0)

plt.close()

img = tiff.imread(os.path.join(save_dir, "pmap.tif"))

H, W = img.shape[:2]

# ===== 输入参数 =====
x0 = 450   # 左下角 x（列）
y0 = 600   # 左下角 y（注意：这是“从下往上”）
w = 400
h = 400

# ===== 坐标转换（关键）=====
# 图像是左上角为原点，所以要转换 y
y_top = H - y0 - h
y_bottom = H - y0

# ===== 裁剪 =====
crop = img[y_top:y_bottom, x0:x0+w]

# ===== 保存 =====
tiff.imwrite(os.path.join(save_dir, "pmap2.tif"), crop)