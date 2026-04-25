import os
import numpy as np
from pathlib import Path
from skimage import io, filters, morphology
from skan import Skeleton, summarize
from scipy.ndimage import distance_transform_edt, binary_fill_holes

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
    result_tifff = os.path.join(output_folder, f"{base_name}_bra.tif").replace("\\", "/")
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

            saveAs("Tiff", "{result_tifff}");

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
            selectWindow("mask_final");
            run("Skeletonize"); 
            run("Analyze Skeleton (2D/3D)", "prune=none calculate");

            // ---- Save ----
            saveAs("Results", "{result_txt}"); 
            saveAs("Tiff", "{result_tif}");

            run("Close All");
            run("Clear Results");
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

def compute_mean_vessel_diameter(binary_mask, skeleton):
    """
    计算平均血管直径（基于 distance transform + skeleton）

    Parameters
    ----------
    binary_mask : 2D ndarray
        血管分割结果（0/1 或 False/True）
    skeleton : 2D ndarray, optional
        skeleton 图。如果为 None，则自动计算
    robust : bool
        是否使用 median（更抗伪影）

    Returns
    -------
    mean_diameter : float
        平均血管直径（像素单位）
    """
    skeleton = skeleton.astype(bool)

    # ===== distance transform =====
    dist = distance_transform_edt(binary_mask)

    # ===== 在 skeleton 上采样半径 =====
    radii = dist[skeleton]

    if len(radii) == 0:
        return 0.0

    # ===== 处理分叉点偏差（可选稳健模式）=====
    radius = np.mean(radii)

    # ===== diameter =====
    mean_diameter = 2.0 * radius

    return mean_diameter

def double_layer_skeletonization_py(full_path, sigma_small=2, sigma_large=12, threshold=0.1):
    # ===== 读取 =====
    full_path = Path(full_path)
    img = io.imread(full_path)

    if img.ndim == 3:
        img = img[..., 0]
    #img = img[..., 0]  # 转灰度

    img = img.astype(np.float32)
    img = (img - img.min()) / (img.max() + 1e-8)

    # ===== 输出路径 =====
    out_dir = full_path.parent / "output_of_skeletonization"
    out_dir.mkdir(exist_ok=True)

    out_dir_a = out_dir / "small"
    out_dir_a.mkdir(exist_ok=True)
    out_dir_b = out_dir / "middle"
    out_dir_b.mkdir(exist_ok=True)
    out_dir_c = out_dir / "large"
    out_dir_c.mkdir(exist_ok=True)
    out_dir_d = out_dir / "merged"
    out_dir_d.mkdir(exist_ok=True)
    out_dir_e = out_dir / "skeleton"
    out_dir_e.mkdir(exist_ok=True)

    base = full_path.stem

    # ===== Tubeness (Frangi) =====
    v_small = filters.frangi(img, sigmas=range(2, 4, 2), black_ridges = False)

    v_middle = filters.frangi(img, sigmas=range(6, 10, 2), black_ridges = False, alpha=0.25, beta=0.25)

    v_large = filters.frangi(img, sigmas=range(12, 16, 2), black_ridges = False, alpha=0.25, beta=0.25)
    
    # ===== 二值化 =====
    mask_small = v_small > 0.1
    mask_middle = v_middle > 0.1
    mask_large = v_large > 0.1

    # ===== 去噪 =====
    mask_small = morphology.remove_small_objects(mask_small, max_size=10)

    mask_middle = morphology.closing(mask_middle, morphology.disk(3))
    mask_middle = morphology.remove_small_objects(mask_middle, max_size=19)

    mask_large = morphology.opening(mask_large, morphology.disk(1))
    mask_large = morphology.erosion(mask_large, morphology.disk(4))
    mask_large = morphology.remove_small_objects(mask_large, max_size=400)
    mask_large = binary_fill_holes(mask_large)

    # ===== 合并 =====
    merged = np.maximum.reduce([mask_small, mask_middle, mask_large])

    # ===== skeleton =====
    skeleton = morphology.skeletonize(merged)
    sk = Skeleton(skeleton)

    # ===== skeleton 分析 =====
    skeleton_stats = summarize(sk, separator='_')

    area = np.sum(merged) / merged.size                                                                                   # 亮像素数量（血管密度）
    branch_count = len(skeleton_stats)                                                                      # 分支总数
    average_branch_length = skeleton_stats["branch_distance"].mean()                                        # 平均分支长度
    mean_diameter = compute_mean_vessel_diameter(merged, skeleton)                                          # 平均血管直径
    tortuosity = (skeleton_stats["branch_distance"] / (skeleton_stats["euclidean_distance"] + 1e-8)).mean() # 曲率

    # ===== 保存 =====
    io.imsave(out_dir / f"merged/{base}_merged.tif", (merged*255).astype(np.uint8))  
    io.imsave(out_dir / f"small/{base}_small.tif", (mask_small*255).astype(np.uint8))
    io.imsave(out_dir / f"middle/{base}_middle.tif", (mask_middle*255).astype(np.uint8))
    io.imsave(out_dir / f"large/{base}_large.tif", (mask_large*255).astype(np.uint8))
    io.imsave(out_dir / f"skeleton/{base}_branch.tif", (skeleton*255).astype(np.uint8))

    return {"area": area, "branch_count": branch_count, "average_branch_length": average_branch_length, "mean_diameter": mean_diameter, "tortuosity": tortuosity}

def double_layer_skeletonization_tem(full_path, sigma_small=2, sigma_large=12, threshold=0.1):
    # ===== 读取 =====
    full_path = Path(full_path)
    img = io.imread(full_path)

    if img.ndim == 3:
        img = img[..., 0]

    #img = img[..., 0]  # 转灰度

    img = img.astype(np.float32)
    img = (img - img.min()) / (img.max() + 1e-8)
    print(type(img))
    print(img.shape)

    # ===== 输出路径 =====
    out_dir = full_path.parent / "output_of_skeletonization"
    out_dir.mkdir(exist_ok=True)

    base = full_path.stem

    # ===== Tubeness (Frangi) =====
    v_small = filters.frangi(img, sigmas=range(1, 2, 2), black_ridges = False)

    v_middle = filters.frangi(img, sigmas=range(6, 10, 2), black_ridges = False, alpha=0.25, beta=0.25)

    v_large = filters.frangi(img, sigmas=range(12, 16, 2), black_ridges = False, alpha=0.25, beta=0.25)
    
    # ===== 二值化 =====
    mask_small = v_small > 0.1
    mask_middle = v_middle > 0.1
    mask_large = v_large > 0.1

    # ===== 去噪 =====
    mask_small = morphology.remove_small_objects(mask_small, max_size=10)

    mask_middle = morphology.closing(mask_middle, morphology.disk(3))
    mask_middle = morphology.remove_small_objects(mask_middle, max_size=19)

    mask_large = morphology.opening(mask_large, morphology.disk(1))
    mask_large = morphology.erosion(mask_large, morphology.disk(4))
    mask_large = morphology.remove_small_objects(mask_large, max_size=400)
    mask_large = binary_fill_holes(mask_large)

    # ===== 合并 =====
    merged = np.maximum.reduce([mask_small, mask_middle, mask_large])

    # ===== skeleton =====
    skeleton = morphology.skeletonize(merged)

    # ===== 保存 =====
    io.imsave(out_dir / f"{base}_merged.tif", (merged*255).astype(np.uint8))  
    io.imsave(out_dir / f"{base}_small.tif", (mask_small*255).astype(np.uint8))
    io.imsave(out_dir / f"{base}_middle.tif", (mask_middle*255).astype(np.uint8))
    io.imsave(out_dir / f"{base}_large.tif", (mask_large*255).astype(np.uint8))
    io.imsave(out_dir / f"{base}_branch.tif", (skeleton*255).astype(np.uint8))
    
    io.imsave(out_dir / f"{base}_small_v.tif", (v_small*255).astype(np.uint8))
    io.imsave(out_dir / f"{base}_middle_v.tif", (v_middle*255).astype(np.uint8))
    io.imsave(out_dir / f"{base}_large_v.tif", (v_large*255).astype(np.uint8))

def double_layer_skeletonization_statistical_purposes_only(full_path, sigma_small=2, sigma_large=12, threshold=0.1):
    # ===== 读取 =====
    full_path = Path(full_path)
    img = io.imread(full_path)

    img = img[..., 0]  # 转灰度

    img = img.astype(np.float32)
    img = (img - img.min()) / (img.max() + 1e-8)

    # ===== Tubeness (Frangi) =====
    v_small = filters.frangi(img, sigmas=range(2, 4, 2), black_ridges = False)

    v_middle = filters.frangi(img, sigmas=range(6, 10, 2), black_ridges = False, alpha=0.25, beta=0.25)

    v_large = filters.frangi(img, sigmas=range(12, 16, 2), black_ridges = False, alpha=0.25, beta=0.25)
    
    # ===== 二值化 =====
    mask_small = v_small > 0.1
    mask_middle = v_middle > 0.1
    mask_large = v_large > 0.1

    # ===== 去噪 =====
    mask_small = morphology.remove_small_objects(mask_small, max_size=10)

    mask_middle = morphology.closing(mask_middle, morphology.disk(3))
    mask_middle = morphology.remove_small_objects(mask_middle, max_size=19)

    mask_large = morphology.opening(mask_large, morphology.disk(1))
    mask_large = morphology.erosion(mask_large, morphology.disk(4))
    mask_large = morphology.remove_small_objects(mask_large, max_size=400)
    mask_large = binary_fill_holes(mask_large)

    # ===== 合并 =====
    merged = np.maximum.reduce([mask_small, mask_middle, mask_large])

    # ===== skeleton =====
    skeleton = morphology.skeletonize(merged)
    sk = Skeleton(skeleton)

    # ===== skeleton 分析 =====
    skeleton_stats = summarize(sk, separator='_')

    area = np.sum(merged)                                                                                   # 亮像素数量（血管密度）
    branch_count = len(skeleton_stats)                                                                      # 分支总数
    average_branch_length = skeleton_stats["branch_distance"].mean()                                        # 平均分支长度
    mean_diameter = compute_mean_vessel_diameter(merged, skeleton)                                          # 平均血管直径
    tortuosity = (skeleton_stats["branch_distance"] / (skeleton_stats["euclidean_distance"] + 1e-8)).mean() # 曲率

    return {"area": area, "branch_count": branch_count, "average_branch_length": average_branch_length, "mean_diameter": mean_diameter, "tortuosity": tortuosity}