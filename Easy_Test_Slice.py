import Image_Reconstruction as ir
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

range1 = [210, 310]

file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Installments\\1_67data.dat'

data = ir.Reconstruction532(file_path)

slice = ir.Slice(data, range1)

print("a")
save_dir = "Output"
cwd = os.getcwd()
save_dir = os.path.join(cwd, save_dir, 'slice11')
os.makedirs(save_dir, exist_ok=True)

for i, s in enumerate(tqdm(slice)):
    plt.figure(figsize=(4,10))
    plt.axis('off')
    # plt.imshow(s, cmap='gist_heat', aspect='auto', vmin=0, vmax=256)
    plt.imshow(s, cmap='gist_heat', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"slice_{i+range1[0]:03d}.tif"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()