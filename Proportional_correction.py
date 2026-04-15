import Image_Reconstruction as ir
from tqdm import tqdm
import imagej
import os

ij = imagej.init('D:/software/fiji-latest-win64-jdk/Fiji', mode='interactive')
def Single_layer_skeletonization(full_path, ij):
    full_path = full_path.replace("\\", "/")

    macro_cmd = f""" 
        open("{full_path}");
        run("Size...", "width=" + 1625 + " height=" + 650 + " interpolation=Bilinear");

        // ---- Save ----
        saveAs("Tiff", "{full_path}");

        run("Close All");
    """
    ij.py.run_macro(macro_cmd)

Single_layer_skeletonization("D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\Group_C\\17.png", ij)