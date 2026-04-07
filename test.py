import Image_Reconstruction.Diverse_images as di
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.colors import hsv_to_rgb

range1 = [180, 280]
range2 = [200,400]
range3 = [220,300]

file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\data.dat'

data = di.Reconstruction532(file_path)

v, h = di.Deep_Encoding(data, range3)

#bscan = di.Bscan(data, range1)
map = di.Map(data)
#slice = di.Slice(data, range2)
P_map = di.Partial_Map(data, range3)

save_dir = "Output"
os.makedirs(save_dir, exist_ok=True)

'''for i, b in enumerate(bscan):

    plt.figure(figsize=(4,12))
    plt.axis('off')
    plt.imshow(b, cmap='gray', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"bscan_{i:03d}.png"),
                dpi=300,
                bbox_inches='tight')

    plt.close()
'''
plt.figure(figsize=(4,10))
plt.imshow(map, cmap='hot', aspect='auto')

plt.savefig(os.path.join(save_dir, f"Map.png"),
            dpi=300,
            bbox_inches='tight')

plt.close()
'''
for i, s in enumerate(slice):

    plt.figure(figsize=(4,10))
    plt.axis('off')
    plt.imshow(s, cmap='hot', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"slice_{i:03d}.png"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()
'''
plt.figure(figsize=(4,10))
plt.axis('off')
plt.imshow(P_map, cmap='hot', aspect='auto')

plt.savefig(os.path.join(save_dir, f"P_Map.png"),
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
            bbox_inches='tight')
