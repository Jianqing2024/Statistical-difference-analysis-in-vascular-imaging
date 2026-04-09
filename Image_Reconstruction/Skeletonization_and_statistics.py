import os
import imagej
from glob import glob

def get_path(folders):
    # 给定一个列表，其中存放所有需要查找的文件夹
    # 用于存放所有文件的列表
    current_dir = os.getcwd()
    all_files = []

    for folder in folders:
        folder_path = os.path.join(current_dir, folder)
        if os.path.exists(folder_path):
            # 查找该文件夹下所有 .tif 文件
            png_files = glob(os.path.join(folder_path, '*.tif'))
            all_files.extend(png_files)  # 添加到总列表
        else:
            print(f"警告: 文件夹不存在 -> {folder_path}")
    return all_files

def Skeletonization(full_path, ij):
    full_path = full_path.replace("\\", "/")
    print(full_path)

    folder = os.path.dirname(full_path)
    output_folder = os.path.join(folder, "output_of_skeletonization").replace("\\", "/")
    os.makedirs(output_folder, exist_ok=True)

    # 获取输入文件名（不带路径和后缀）
    base_name = os.path.splitext(os.path.basename(full_path))[0]

    # 输出文件路径
    result_txt = os.path.join(output_folder, f"{base_name}_branch.txt").replace("\\", "/")
    result_tif = os.path.join(output_folder, f"{base_name}_branch.tif").replace("\\", "/")
    result_den_txt = os.path.join(output_folder, f"{base_name}_den.txt").replace("\\", "/")
    result_den_tif = os.path.join(output_folder, f"{base_name}_den.tif").replace("\\", "/")

    # full_path 是完整路径，如 D:/WORK/GYY/tumer/abc.png
    # ImageJ 窗口名必须是文件名本身
    # 该函数暂时不支持进行比例矫正
    img_name = os.path.basename(full_path)

    macro_cmd = f""" 
        open("{full_path}");
        selectWindow("{img_name}");
        //如需进行比例矫正,请为以下代码取消注释
        //w = getWidth();
        //h = getHeight();

        //target_h = w * 5 / 4;
        //run("Size...", "width=" + w + " height=" + target_h + " interpolation=Bilinear");

        // ---- Small vessels ----
        run("8-bit"); 
        //setAutoThreshold("Otsu dark");
        run("Tubeness", "sigma=5 black");
        run("Convert to Mask");
        rename("mask_small");
        run("Duplicate...", "title=mask_small_copy");

        // ---- Large vessels ----
        selectWindow("{img_name}");
        run("8-bit"); 
        //setAutoThreshold("Otsu dark");
        run("Tubeness", "sigma=10 black");
        run("Convert to Mask");
        rename("mask_large");
        run("Duplicate...", "title=mask_large_copy");

        // ---- Combine masks ----
        imageCalculator("OR create", "mask_small_copy", "mask_large_copy");
        rename("mask_final");
        selectWindow("mask_final");
        saveAs("Tiff", "{result_den_tif}");
        // 设置测量参数
        run("Set Scale...", "distance=1 known=1 pixel=1 unit=pixel");
        //run("Set Measurements...", "area redirect=None decimal=3");
        run("Set Measurements...", "area redirect=None decimal=0");

        // 计算所有血管区域面积（并汇总）
        run("Analyze Particles...", "size=0-Infinity summarize");

        // 导出结果(Summary 里包含 Total Area)
        saveAs("Results", "{result_den_txt}");

        // ---- Skeleton analysis ----
        run("Skeletonize"); 
        run("Analyze Skeleton (2D/3D)", "prune=none calculate");

        // ---- Save ----
        saveAs("Results", "{result_txt}"); 
        saveAs("Tiff", "{result_tif}");

        run("Close All");
    """ 
    ij.py.run_macro(macro_cmd)