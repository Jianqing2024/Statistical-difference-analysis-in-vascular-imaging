import numpy as np
from scipy.signal import hilbert
from scipy.ndimage import median_filter

def Reconstruction(file_path, mod=1):
    shape = (1500, 1250, 2048)

    data = np.fromfile(file_path, dtype=np.int16)
    data = data.reshape(shape).astype(np.float32)

    if 1 in mod:
        Mod1 = data[:,:,0:512]
    if 2 in mod:
        Mod2 = data[:,:,512:1024]
    if 3 in mod:
        Mod3 = data[:,:,1024:2048]

    return [Mod1, Mod2, Mod3]

def Enhancement(Mod):
    for data in Mod:
        mean_profile = np.mean(data, axis=2)
        data = data - mean_profile


    return envelope