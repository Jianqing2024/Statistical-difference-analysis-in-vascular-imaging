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

def Double_layer_skeletonization(full_path, ij, sigma_min = 2, sigma_large = 8):
    # 此函数与单层骨架化的区别在于，在区间较大的MAP图中，有多种大小不同的血管，通过两层sigma值尽量读取到更多的血管
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
    result_den_txt = os.path.join(output_folder, f"{base_name}_density.txt").replace("\\", "/")
    result_den_tif = os.path.join(output_folder, f"{base_name}_density.tif").replace("\\", "/")

    # full_path 是完整路径，如 D:/WORK/GYY/tumer/abc.png
    # ImageJ 窗口名必须是文件名本身
    # 该函数暂时不支持进行比例矫正
    img_name = os.path.basename(full_path)


    macro_cmd = f""" 
            open("{full_path}");
            selectWindow("{img_name}");
            
            run("8-bit"); 
            rename("im");

            selectWindow("im");
            run("Tubeness", "sigma={sigma_min}");
            rename("mask_small");
            run("Duplicate...", "title=mask_small_copy");

            selectWindow("im");
            run("Tubeness", "sigma={sigma_large}");
            rename("mask_large");
            run("Duplicate...", "title=mask_large_copy");

            // ---- Combine masks ----
            imageCalculator("Max create", "mask_small_copy", "mask_large_copy");
            rename("mask_final");
            run("8-bit");
            setThreshold(20, 255);
            run("Convert to Mask");

            run("Remove Outliers...", "radius=3 threshold=30 which=Bright");
            run("Despeckle");

            saveAs("Tiff", "{result_den_tif}");
            // 设置测量参数
            rename("mask_final");
            selectWindow("mask_final");
            run("Set Scale...", "distance=1 known=1 pixel=1 unit=pixel");
            run("Set Measurements...", "area redirect=None decimal=3");
            run("Set Measurements...", "area redirect=None decimal=0");

            // 计算所有血管区域面积（并汇总）
            run("Analyze Particles...", "size=0-Infinity summarize");

            // 导出结果(Summary 里包含 Total Area)
            saveAs("Results", "{result_den_txt}");

            // ---- Skeleton analysis ----
            //rename("mask_final");
            selectWindow("mask_final");
            run("Skeletonize"); 
            run("Analyze Skeleton (2D/3D)", "prune=none calculate");

            // ---- Save ----
            saveAs("Results", "{result_txt}"); 
            saveAs("Tiff", "{result_tif}");

            run("Close All");
    """
    ij.py.run_macro(macro_cmd)

def Single_layer_skeletonization(full_path, ij, sigma_min):
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
    result_den_txt = os.path.join(output_folder, f"{base_name}_density.txt").replace("\\", "/")
    result_den_tif = os.path.join(output_folder, f"{base_name}_density.tif").replace("\\", "/")

    # full_path 是完整路径，如 D:/WORK/GYY/tumer/abc.png
    # ImageJ 窗口名必须是文件名本身
    # 该函数暂时不支持进行比例矫正
    img_name = os.path.basename(full_path)

    macro_cmd = f""" 
        open("{full_path}");
        selectWindow("{img_name}");
        
        rename("mask_final");
        selectWindow("mask_final");
        //如需进行比例矫正,请为以下代码取消注释
        //w = getWidth();
        //h = getHeight();

        //target_h = w * 5 / 4;
        //run("Size...", "width=" + w + " height=" + target_h + " interpolation=Bilinear");

        run("8-bit"); 
        run("Tubeness", "sigma={sigma_min}");
        rename("mask_final");
        selectWindow("mask_final");

        setAutoThreshold("Otsu");
        rename("mask_final");
        selectWindow("mask_final");

        //setAutoThreshold();
        run("Convert to Mask");
        rename("mask_final");
        selectWindow("mask_final");

        run("Duplicate...", "title=mask_small_copy");
        rename("mask_final");
        selectWindow("mask_final");

        // 修改部分
        // ---- Step 1: 强力去孤立点 ----
        //run("Remove Outliers...", "radius=2 threshold=30 which=Bright");
        //run("Despeckle");

        // ---- Step 2: 去掉小连通域（非常关键）----
        run("Analyze Particles...", "size=50-Infinity show=Masks clear");
        run("Dilate");
        run("Dilate");

        // ---- Step 3: 补血管 ----
        run("Close");   // 填小断裂

        // ---- Step 4: 平滑 ----
        run("Gaussian Blur...", "sigma=1");
        setAutoThreshold("Otsu");
        run("Convert to Mask");

        // ---- Step 5: 轻微去粘连 ----
        run("Open");
        // ---------------------------

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
        rename("mask_final");
        selectWindow("mask_final");
        run("Skeletonize"); 
        run("Analyze Skeleton (2D/3D)", "prune=none");

        // ---- Save ----
        saveAs("Results", "{result_txt}"); 
        saveAs("Tiff", "{result_tif}");

        run("Close All");
    """
    ij.py.run_macro(macro_cmd)