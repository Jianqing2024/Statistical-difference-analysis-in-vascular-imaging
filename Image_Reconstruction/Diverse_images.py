import numpy as np
from .Basic_computation import *

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
        slice.append(nonlinear_cuda_style(data[:,:,i]))
        #slice.append(data[:,:,i])
    return slice

def Partial_Map(data, Range):
    # data为原始数据，range为一列表，标记了所需Bscan的起止索引
    data = data[:,:,Range[0]:Range[1]]
    map = np.max(data, axis=2)
    map = nonlinear_cuda_style(map)
    return map

def Deep_Encoding(data, Range):
    # data为原始数据，range为一列表，标记了所需Bscan的起止索引
    # 输出亮度/颜色
    data = data[:,:,Range[0]:Range[1]]
    argmap = np.argmax(data, axis=2)
    map = np.take_along_axis(data, argmap[:, :, np.newaxis], axis=2).squeeze(axis=2)
    # 增强和归一化
    map = nonlinear_cuda_style(map,light= 50)
    map = (map - map.min()) / (map.max() - map.min())
    argmap = (argmap - argmap.min()) / (argmap.max() - argmap.min())
    return map, argmap


file_path = 'D:\\WORK\\Statistical-difference-analysis-in-vascular-imaging\\37data.dat'

data = Reconstruction532(file_path)