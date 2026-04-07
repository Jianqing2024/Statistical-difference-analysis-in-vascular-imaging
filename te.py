import cupy as cp
from cupyx.scipy.ndimage import median_filter, uniform_filter1d
import numpy as np
import matplotlib.pyplot as plt

def Reconstruction(file_path):
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
    mean_aline = cp.mean(data, axis=2, keepdims=True)
    data = data - mean_aline

    # -------- 2. 5点中值滤波 --------
    data = median_filter(data, size=(1, 1, 5), mode='nearest')

    # -------- 3. Wiener（向量化）--------
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
    '''
    # -------- 4. log压缩 --------
    data = cp.abs(data)
    data = 20 * cp.log10(data + 1e-6)

    # -------- 5. 归一化 --------
    data -= data.min()
    data /= (data.max() + 1e-8)

    data = (data * 255).astype(cp.uint8)
    '''
    # -------- 6. 回CPU（可选）--------
    return cp.asnumpy(data)

def nonlinear_cuda_style(mip,light=0,percent=50,noise=0,gain=0):

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

    # -----------------------------
    # 亮度调整
    # -----------------------------
    mip = mip + light

    # -----------------------------
    # 对比度拉伸（围绕127）
    # -----------------------------
    mip = 127 + (mip - 127) / a

    # -----------------------------
    # 裁剪
    # -----------------------------
    mip = np.clip(mip, 0, 255)

    return mip.astype(np.uint8)

data = Reconstruction('37data.dat')
data = Enhancement_GPU(data)

mip = np.max(data, axis=2)

mip = nonlinear_cuda_style(mip)

save_dir = "stay"

plt.figure(figsize=(4,10))

plt.imshow(
    mip,
    cmap='hot',
    aspect='auto'   # 或 'equal'
)
plt.yticks(np.arange(0, 1500, 100))

plt.xlabel("A-line (pixel)")
plt.ylabel("B-scan (pixel)")
plt.title("Maximum Projection (Pixel Coordinates)")
plt.show()