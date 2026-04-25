import numpy as np
from .Basic_computation import *
from .Tools import *

def Bscan(data, Range):
    # data为原始数据，range为一列表，标记了所需Bscan的起止索引
    data = data[Range[0]:Range[1],:,:]
    data = Enhancement_GPU(data)
    bscan = []
    for i in range(Range[1]-Range[0]):
        bscan.append(nonlinear_cuda_style(data[i,:,:]))
        #bscan.append(data[i,:,:])
    return bscan

def Map(data):
    data = Enhancement_GPU(data)
    map = np.max(data, axis=2)
    map = nonlinear_cuda_style(map)
    return map

def Slice(data, Range):
    # data为原始数据，range为一列表，标记了所需Bscan的起止索引
    data = Enhancement_GPU(data)
    slice = []
    for i in range(Range[1]-Range[0]):
        sl = simple_nonlinear(data[:,:,i+Range[0]], gamma=1.2)
        #sl = nonlinear_cuda_style(data[:,:,i+Range[0]],light=-135)
        slice.append(sl)
    return slice

def Partial_Map(data, Range, size):
    List = split_range(Range[0], Range[1], size)
    P_Map = []
    data = data[:,:,Range[0]:Range[1]]
    data = Enhancement_GPU(data)

    for l in List:
        data_use = data[:,:,(l[0]-Range[0]):(l[1]-Range[0])]
        map = np.max(data_use, axis=2)
        map = simple_nonlinear(map, gamma=2)

        P_Map.append(map)
    return P_Map

def Deep_Encoding(data, Range):
    # data为原始数据，range为一列表，标记了所需Bscan的起止索引
    # 输出亮度/颜色
    data = Enhancement_GPU(data)
    data = data[:,:,Range[0]:Range[1]]
    argmap = np.argmax(data, axis=2)
    map = np.take_along_axis(data, argmap[:, :, np.newaxis], axis=2).squeeze(axis=2)
    # 增强和归一化
    map = nonlinear_cuda_style(map,light= 0)
    map = (map - map.min()) / (map.max() - map.min())
    argmap = (argmap - argmap.min()) / (argmap.max() - argmap.min())
    return map, argmap
