from vtk.util.vtkImageImportFromArray import *
import vtk
import SimpleITK as sitk
import numpy as np
import time

path = 'E:\\111\\DATA_nii\\case_00039\\imaging.nii.gz'  # segmentation volume
ds = sitk.ReadImage(path)  # 读取nii数据的第一个函数sitk.ReadImage
print('ds: ', ds)
data = sitk.GetArrayFromImage(ds)  # 把itk.image转为array
print('data: ', data)
print('shape_of_data', data.shape)

spacing = ds.GetSpacing()  # 三维数据的间隔
print('spacing_of_data', spacing)

srange = [np.min(data), np.max(data)]
print('shape_of_data_chenged', data.shape)

