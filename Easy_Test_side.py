import Image_Reconstruction as ir
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

range1 = [210, 310]

file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Installments\\1_67data.dat'

data = ir.Reconstruction532(file_path)

map = ir.Deep_Side(data, 10)

print("a")

plt.figure(figsize=(4,10))
plt.axis('off')
# plt.imshow(s, cmap='gist_heat', aspect='auto', vmin=0, vmax=256)
plt.imshow(map, cmap='gist_heat', aspect='auto')

plt.savefig(os.path.join("ppp.tif"),
            dpi=300,
            bbox_inches='tight',
            pad_inches=0)