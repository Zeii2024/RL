import os
import cv2
import numpy as np

def getData(path):
    '''
    该函数得到每个案例下的数据
    :param path: 案例的路径
    :return: 切片列表，Ground Truth列表
    '''
    gt = path+'/GT/'
    img = path + '/Images/'

    gts = os.listdir(gt)
    gts = [str(gt) + name for name in gts]

    images = os.listdir(img)
    images = [str(img) + name for name in images]

    return images,gts
def getLabel(gts):
    '''
    该函数得到案例中每张切片是否存在肿瘤
    :param gts: Ground Truth列表
    :return: (切片标签,类别)
    '''
    labels = []
    for i in range(len(gts)):
        t = cv2.imread(gts[i],0)
        if t.__contains__(255) == True:
            labels.append((gts[i],2))
        elif t.__contains__(128) == True:
            labels.append((gts[i],1))
        else:
            labels.append((gts[i],0))
    return labels
def utils_numOfTumor(path):
    x, y = getData(path)
    labels = getLabel(y)

    t = [y for x, y in labels]
    t = np.array(t)
    tumor_num = np.sum(t == 2)
    kidney_num = np.sum(t == 1) + tumor_num
    black_num = np.sum(t == 0)

    return tumor_num,kidney_num,black_num