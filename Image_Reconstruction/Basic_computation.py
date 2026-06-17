import cupy as cp
from cupyx.scipy.ndimage import median_filter, uniform_filter1d
import numpy as np

def hilbert_envelope_gpu(data):
    """
    沿 axis=2 (Sample方向) 做 Hilbert 包络
    """
    N = data.shape[2]

    # FFT
    Xf = cp.fft.fft(data, axis=2)

    # 构造 Hilbert 滤波器
    h = cp.zeros(N, dtype=cp.float32)

    if N % 2 == 0:
        h[0] = 1
        h[N//2] = 1
        h[1:N//2] = 2
    else:
        h[0] = 1
        h[1:(N+1)//2] = 2

    # 应用滤波器
    Xf = Xf * h[None, None, :]

    # IFFT → analytic signal
    analytic = cp.fft.ifft(Xf, axis=2)

    # 包络
    envelope = cp.abs(analytic)

    return envelope

def detect_outliers_std(data, k=10):
    mean = cp.mean(data)
    std = cp.std(data)

    lower = mean - k * std
    upper = mean + k * std

    mask = (data < lower) | (data > upper)
    data[mask] = 0
    return data

def Reconstruction532(file_path):
    shape = (1500, 1250, 2048)

    data = np.fromfile(file_path, dtype=np.int16)
    data = data.reshape(shape).astype(np.float32)

    Mod1 = data[:,:,0:512] # 只选取532模态

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
    # 去除异常点
    data = detect_outliers_std(data, k=5)

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

    # -------- 4. 包络检测 --------
    data = hilbert_envelope_gpu(data)

    return cp.asnumpy(data)

def simple_nonlinear(mip, gamma=0.7):
    mip = mip - mip.min()
    mip = mip / (mip.max() + 1e-8)

    mip = mip ** gamma   # 非线性增强

    mip = (mip * 255).astype(np.uint8)
    mip = np.clip(mip, 0, 255)

    return mip.astype(np.uint8)

def nonlinear_cuda_style(mip,light=0,percent=50,noise=1e-6,gain=0):

    # -------- 5. 归一化 --------
    mip -= mip.min()
    mip /= (mip.max() + 1e-8)
    #mip = (mip * 255).astype(cp.uint8)
    mip = mip * 255

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

    mip -= mip.min()
    mip /= mip.max()
    mip = (mip * 255)
    mip = (mip + light)
    mip = np.clip(mip, 0, 255)

    return mip.astype(np.uint8)

'''
def nonlinear_cuda_style(mip, light=0, percent=50, noise=1e-6, gain=0):
    """
    改进版 log 压缩
    适用于已归一化或 uint8 数据（0~255）
    """

    # -------- 1. 转 float --------
    mip = mip.astype(np.float32)

    # -------- 2. 可选：轻微抬底（避免全黑）--------
    mip = mip + noise

    # -------- 3. log 压缩（核心修正）--------
    # k 控制压缩强度（类似 gamma）
    k = 0.02 - gain / 10000.0
    k = max(k, 1e-6)

    mip = np.log1p(k * mip)

    # -------- 4. 亮度调整 --------
    mip = mip + light

    # -------- 5. 百分位拉伸（替代你原来的 percent 逻辑）--------
    low_p = percent / 2
    high_p = 100 - percent / 2

    low = np.percentile(mip, low_p)
    high = np.percentile(mip, high_p)

    mip = np.clip(mip, low, high)

    # -------- 6. 归一化 --------
    mip = mip - mip.min()
    mip = mip / (mip.max() + 1e-12)

    # -------- 7. 转 uint8 --------
    mip = (mip * 255).astype(np.uint8)

    return mip
'''