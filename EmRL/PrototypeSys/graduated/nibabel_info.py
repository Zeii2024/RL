# encoding=utf8
'''
查看和显示nii文件
'''

import matplotlib
# matplotlib.use('TkAgg')

import nibabel as nib
from nibabel import nifti1
from nibabel.viewers import OrthoSlicer3D

example_filename = 'E:\\111\\DATA_nii\\case_00039\\imaging.nii.gz'
# example_filename = 'E:\\111\\DATA_nii\\case_00039\\segmentation.nii'

img = nib.load(example_filename)
print(img)
print('----------')
print(type(img))
print('----------')
print(img.shape)
print('----------')
print(img.header['sizeof_hdr'])


width, height, queue = img.dataobj.shape
OrthoSlicer3D(img.dataobj).show()
