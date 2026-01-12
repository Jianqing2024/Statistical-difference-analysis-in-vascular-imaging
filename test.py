import os
from glob import glob
import imagej

ij = imagej.init('D:/software/fiji-latest-win64-jdk/Fiji', mode='interactive')

def creatCMD(full_path, result_txt, result_png):
    # full_path 是完整路径，如 D:/WORK/GYY/tumer/abc.png
    # ImageJ 窗口名必须是文件名本身
    img_name = os.path.basename(full_path)

    macro_cmd = f""" 
        open("{full_path}");
        selectWindow("{img_name}");

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
        run("Tubeness", "sigma=9 black");
        run("Convert to Mask");
        rename("mask_large");
        run("Duplicate...", "title=mask_large_copy");

        // ---- Combine masks ----
        imageCalculator("OR create", "mask_small_copy", "mask_large_copy");
        rename("mask_final");
        selectWindow("mask_final");

        // ---- Skeleton analysis ----
        run("Skeletonize"); 
        run("Analyze Skeleton (2D/3D)", "prune=none calculate");

        // ---- Save ----
        saveAs("Results", "{result_txt}"); 
        saveAs("PNG", "{result_png}");

        run("Close All");
    """ 
    return macro_cmd


def run_fiji(ij, base_name, result_txt, result_png):

    # 拼接宏命令
    macro_cmd = creatCMD(base_name, result_txt, result_png)

    # 打印宏命令，方便调试
    print("执行宏命令:\n", macro_cmd)

    # 执行宏
    ij.py.run_macro(macro_cmd)

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 目标子文件夹
folders = ['tumer', 'normal']

# 用于存放所有文件的列表
all_files = []

for folder in folders:
    folder_path = os.path.join(current_dir, folder)
    if os.path.exists(folder_path):
        # 查找该文件夹下所有 .png 文件
        png_files = glob(os.path.join(folder_path, '*.png'))
        all_files.extend(png_files)  # 添加到总列表
    else:
        print(f"警告: 文件夹不存在 -> {folder_path}")

print(all_files)

for file in all_files:
    file = file.replace("\\", "/")
    print(file)
    folder = os.path.dirname(file)
    output_folder = os.path.join(folder, "output").replace("\\", "/")
    os.makedirs(output_folder, exist_ok=True)

    # 获取输入文件名（不带路径和后缀）
    base_name = os.path.splitext(os.path.basename(file))[0]

    # 输出文件路径
    result_txt = os.path.join(output_folder, f"{base_name}_branch.txt").replace("\\", "/")
    result_png = os.path.join(output_folder, f"{base_name}_branch.png").replace("\\", "/")

    run_fiji(ij, file, result_txt, result_png)