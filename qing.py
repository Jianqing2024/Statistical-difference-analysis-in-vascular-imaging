import cupy as cp
from cupyx.scipy.ndimage import median_filter, uniform_filter1d
import numpy as np
import os
import matplotlib.pyplot as plt

def Map(data):
    data = Enhancement_GPU(data)
    map = np.max(data, axis=2)
    map = nonlinear_cuda_style(map)
    return map

def mapp(data):
    return np.max(data, axis=2)

def paint(mip, i):
    import os
    import matplotlib.pyplot as plt

    save_dir = "output2"
    os.makedirs(save_dir, exist_ok=True)

    plt.figure(figsize=(4,10))
    plt.axis('off')
    plt.imshow(mip.get(), cmap='hot', aspect='auto')  # <-- 注意这里

    plt.savefig(os.path.join(save_dir, f"slice_{i:03d}.png"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)
    plt.close()

def paint2(mip, i):
    save_dir = "output2"
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(4,10))
    plt.axis('off')
    #plt.imshow(mip.get(mip), cmap='hot', aspect='auto')
    plt.imshow(mip, cmap='hot', aspect='auto')

    plt.savefig(os.path.join(save_dir, f"slice_{i:03d}.png"),
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    plt.close()

def detect_outliers_std(data, k=10):
    mean = np.mean(data)
    std = np.std(data)

    lower = mean - k * std
    upper = mean + k * std

    mask = (data < lower) | (data > upper)
    #print("阈值:", lower, upper)
    #print("异常点占比:", np.sum(mask)/np.size(data))
    data[mask] = 0
    return data

def Reconstruction532(file_path):
    shape = (1500, 1250, 2048)

    data = np.fromfile(file_path, dtype=np.int16)
    data = data.reshape(shape).astype(np.float32)

    Mod1 = data[:,:,0:512]

    return Mod1

def Enhancement_GPU(data):
    """
    GPU版本增强函数
    data: numpy.ndarray or cupy.ndarray
          shape = (Bscan, Aline, Sample)
    """
    # -------- 0. 转到GPU --------
    if not isinstance(data, cp.ndarray):
        data = cp.asarray(data, dtype=cp.float32)
    else:
        data = data.astype(cp.float32)

    # -------- 1. Aline方向减直流 --------
    map = mapp(data)
    paint(map, 1)
    mean_aline = cp.mean(data, axis=2, keepdims=True)
    data = data - mean_aline
    # 去除异常点
    data = detect_outliers_std(data, k=5)

    # -------- 2. 5点中值滤波 --------
    map = mapp(data)
    paint(map, 2)
    data = median_filter(data, size=(1, 1, 5), mode='nearest')

    # -------- 3. Wiener（向量化）--------
    map = mapp(data)
    paint(map, 3)
    radius = 7
    size = 2 * radius + 1

    # 局部均值
    local_mean = uniform_filter1d(data, size=size, axis=2, mode='nearest')

    # 局部平方均值
    local_mean_sq = uniform_filter1d(data**2, size=size, axis=2, mode='nearest')

    # 局部方差
    local_var = local_mean_sq - local_mean**2

    # 噪声估计（沿Aline平均）
    noise_var = cp.mean(local_var, axis=2, keepdims=True)

    # Wiener增益
    gain = cp.maximum(0, local_var - noise_var) / (local_var + 1e-8)
    
    # 输出
    data = local_mean + gain * (data - local_mean)

    # -------- 6. 回CPU（可选）--------
    return cp.asnumpy(data)

def nonlinear_cuda_style(mip,light=0,percent=50,noise=1e-6,gain=0):
    paint2(mip, 4)

    # -------- 5. 归一化 --------
    mip -= mip.min()
    mip /= (mip.max() + 1e-8)

    mip = (mip * 255).astype(cp.uint8)

    # 参数
    k = 0.02 - gain / 10000.0
    a = 1.0 - percent / 100.0

    # 防止非法
    k = max(k, 1e-6)
    a = max(a, 1e-3)

    # -----------------------------
    # 非线性 log 压缩（统一log底）
    # -----------------------------
    mip = np.log1p((mip + noise) * k) / np.log1p(k)
    #print(np.max(mip))
    #print(np.min(mip))

    # -----------------------------
    # 对比度拉伸（围绕127）
    # -----------------------------
    #mip = 127 + (mip - 127) / a

    # -----------------------------
    # 裁剪
    # -----------------------------
    mip -= mip.min()
    mip /= mip.max()
    mip = (mip * 255).astype(np.uint8)
    mip = mip + light
    mip = np.clip(mip, 0, 255)
    paint2(mip, 5)

    return mip.astype(np.uint8)

file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\data.dat'

data = Reconstruction532(file_path)
map = Map(data)