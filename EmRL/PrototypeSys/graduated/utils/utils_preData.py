import os
import cv2

def utils_retCopy(pic_input):
    pic_gt = str(pic_input).replace("Images", "GT")

    dir = pic_input.split('\\')
    dir = "\\".join(dir[:-2])

    if not os.path.exists(dir+'/tmp/Images'):
        os.makedirs(dir+'/tmp/Images')
    if not os.path.exists(dir+'/tmp/GT'):
        os.makedirs(dir+'/tmp/GT')

    image = cv2.imread(pic_input, 0)
    gt = cv2.imread(pic_gt,0)

    ret_img = dir + "\\tmp\\Images\\" + pic_input.split("\\")[-1]
    ret_gt = dir + "\\tmp\\GT\\" + pic_gt.split("\\")[-1]

    cv2.imwrite(ret_img, image)
    cv2.imwrite(ret_gt, gt)

    return ret_img

def utils_flippedHorizontally(img):
    image = cv2.imread(img,0)
    temp = cv2.flip(image,1)
    cv2.imwrite(img,temp)

def utils_flippedVertical(img):
    image = cv2.imread(img,0)
    temp = cv2.flip(image,0)
    cv2.imwrite(img,temp)

def utils_rotation(img):
    image = cv2.imread(img, 0)
    row, col = image.shape
    temp = cv2.getRotationMatrix2D((col / 2, row / 2), 45, 1)
    dst = cv2.warpAffine(image, temp, (col, row))
    cv2.imwrite(img, dst)

def utils_cropScale(img):
    image = cv2.imread(img, 0)
    image = image[40:230, 25:255]
    image = cv2.resize(image, (248, 248))
    cv2.imwrite(img, image)

'''
# dir = "E:\\111\\DATA_nii_out\\case_00039\\"

def utils_flippedHorizontally(dir,img):
    if not os.path.exists(dir+'/temp'):
        os.makedirs(dir+'/temp')
    image = cv2.imread(img,0)
    temp = cv2.flip(image,1)
    name = dir +'/temp/'+str(int(str(img).split('\\')[-1].split('.')[0])+1000)+'.jpg'
    cv2.imwrite(name,temp)

def utils_flippedVertical(dir,img):
    if not os.path.exists(dir + '/temp'):
        os.makedirs(dir + '/temp')
    image = cv2.imread(img,0)
    temp = cv2.flip(image,0)
    name = dir +'/temp/'+str(int(str(img).split('\\')[-1].split('.')[0])+2000)+'.jpg'
    cv2.imwrite(name,temp)

def utils_rotation(dir,img):
    if not os.path.exists(dir + '/temp'):
        os.makedirs(dir + '/temp')
    image = cv2.imread(img, 0)
    row, col = image.shape
    temp = cv2.getRotationMatrix2D((col / 2, row / 2), 45, 1)
    dst = cv2.warpAffine(image, temp, (col, row))
    name = dir +'/temp/'+str(int(str(img).split('\\')[-1].split('.')[0])+3000)+'.jpg'
    cv2.imwrite(name, dst)

def utils_cropScale(dir,img):
    if not os.path.exists(dir+'/temp'):
        os.makedirs(dir+'/temp')
    image = cv2.imread(img, 0)
    image = image[40:230, 25:255]
    image = cv2.resize(image, (248, 248))
    name = dir +'/temp/'+str(int(str(img).split('\\')[-1].split('.')[0])+4000)+'.jpg'
    cv2.imwrite(name, image)
'''

# img = "E:\\111\\DATA_nii_out\\case_00039\\Images\\0030.jpg"
# ret = utils_retCopy(img)
# print(ret)
# utils_flippedHorizontally(ret)
# utils_flippedVertical(ret)
# utils_rotation(ret)
# utils_cropScale(ret)