import Image_Reconstruction as ir
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from pathlib import Path

# file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\data_CT26.dat'

folder = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\B-scan'

dat_files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.endswith(".dat")
]
print(dat_files)

for i, f in enumerate(tqdm(dat_files)):
    print(f)

    data = ir.Reconstruction532(f)

    P_map = ir.Partial_Map(data, [215, 260], 45)
    name = os.path.basename(f)
    name = Path(name).stem
    print("a")
    save_dir = "Output"
    save_dir2 = "p_map"
    cwd = os.getcwd()
    save_dir = os.path.join(cwd, save_dir, save_dir2)
    os.makedirs(save_dir, exist_ok=True)

    for j, p in enumerate(tqdm(P_map)):
        plt.figure(figsize=(4,10))
        plt.axis('off')
        plt.imshow(p, cmap='gist_heat', aspect='auto', vmin=0, vmax=255)

        plt.savefig(os.path.join(save_dir, f"P_map_{name}.tif"),
                    dpi=300,
                    bbox_inches='tight',
                    pad_inches=0)

        plt.close()