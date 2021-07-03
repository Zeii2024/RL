import os
import cv2
import numpy as np
import nibabel as nib
import scipy.ndimage as nd
import matplotlib.pyplot as plt

def resample(img, seg, scan, new_voxel_dim):
    # 进行重采样
    # Get voxel size
    voxel_dim = np.array(scan.header.structarr["pixdim"][1:4], dtype=np.float32)
    # print('voxel_dim',voxel_dim)
    # Resample to optimal [1,1,1] voxel size
    resize_factor = voxel_dim / new_voxel_dim
    scan_shape = np.array(scan.header.get_data_shape())
    new_scan_shape = scan_shape * resize_factor
    rounded_new_scan_shape = np.round(new_scan_shape)
    rounded_resize_factor = rounded_new_scan_shape / scan_shape  # Change resizing due to round off error
    new_voxel_dim = voxel_dim / rounded_resize_factor

    img = nd.interpolation.zoom(img, rounded_resize_factor, mode='nearest')
    seg = nd.interpolation.zoom(seg, rounded_resize_factor, mode='nearest')
    # print('new_voxel_dim',new_voxel_dim)
    # print('img.shape',img.shape)
    return img, seg, new_voxel_dim
def load_volume(case_path):
    # 加载Image
    vol = nib.load(str(case_path + "imaging.nii.gz"))
    return vol
def load_segmentation(case_path):
    # 加载Ground Truth
    seg = nib.load(str(case_path + "segmentation.nii.gz"))
    return seg
def oneReSampled(case,path,path_output,gap):
    # 一个案例要进行的操作
    path_load = path + '\\'
    path_save = path_output + '\\'+ case + '\\'

    if not os.path.exists(path_save+'Images/'):
        os.makedirs(path_save+'Images/')

    if not os.path.exists(path_save+'GT/'):
        os.makedirs(path_save+'GT/')

    img_scan = load_volume(path_load)
    seg_scan = load_segmentation(path_load)
    img = np.asanyarray(img_scan.dataobj)
    seg = np.asanyarray(seg_scan.dataobj)

    img, gt, dim = resample(img, seg, img_scan, gap)
    img = np.where(img < -90, -90, img)
    img = np.where(img > 310, 310, img)
    img = ((img - 101) / 76.9) * 255

    for i in range(img.shape[0]):
        name_img = path_save + 'Images/' + str(i).zfill(4) + '.jpg'
        temp_img = img[i]
        cv2.resize(temp_img,(248,248))
        plt.imsave(name_img, temp_img, cmap='Greys_r')

        name_gt = path_save + 'GT/' + str(i).zfill(4) + '.jpg'
        temp_gt = gt[i]
        temp_gt = np.where(temp_gt == 1, 127, temp_gt)
        temp_gt = np.where(temp_gt == 2, 255, temp_gt)
        cv2.resize(temp_img, (248, 248))
        cv2.imwrite(name_gt, temp_gt)

def utils_getReSampled(path_input,path_output,gap):
    case = path_input.split('\\')[-1]
    gaps = [float(x) for x in gap.split(',')]
    oneReSampled(case,path_input,path_output,gaps)
    return case

def utils_delFullBlack(path_output,case):
    dir = path_output + "/" + case + "/"
    temp = os.listdir(dir+'GT/')
    gts = [dir+'GT/'+x for x in temp]
    imgs  = [dir+'Images/'+x for x in temp]

    for i,item in enumerate(gts):
        t = cv2.imread(item, 0)
        if t.__contains__(127) == True:
            print('exist',item)
        else:
            if os.path.exists(item):
                os.remove(item)
                os.remove(imgs[i])
            else:
                print('no exist')

if __name__ == "__main__":
    pass
    # path_output = "E:\\111\\DATA_nii_out"
    # case = "case_00039"
    # utils_delFullBlack(path_output,case)
