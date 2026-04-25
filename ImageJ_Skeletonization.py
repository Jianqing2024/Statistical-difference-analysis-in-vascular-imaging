import Image_Reconstruction as ir
from tqdm import tqdm
import imagej
import os

ij = imagej.init('D:/software/fiji-latest-win64-jdk/Fiji', mode='interactive')
save_dir = "Output"
cwd = os.getcwd()
save_dir = os.path.join(cwd, save_dir)
os.makedirs(save_dir, exist_ok=True)

files = ir.get_path([save_dir])

for file in tqdm(files):
    ir.Double_layer_skeletonization(file, ij)