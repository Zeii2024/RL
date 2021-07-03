import matplotlib
matplotlib.use('TkAgg')
import nibabel as nib
from nibabel.viewers import OrthoSlicer3D

example_filename = 'E:\\111\\DATA_nii\\case_00039\\imaging.nii.gz'

img = nib.load(example_filename)
print(type(img.dataobj))

t = OrthoSlicer3D(img.dataobj)
t.show()

