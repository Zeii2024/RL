import os
import cv2
import random
import numpy as np

PATH = 'F:/Datasets_IMAGE/temp/DATA/'
dir = 'F:/Datasets_IMAGE/temp/'
path_test = "F:/Datasets_IMAGE/KITS2020/DATA/case_00005/"

###删除全黑切片###
def loadFullCase(path=PATH):
    # 得到所有案例名称
    fullCase = os.listdir(path)
    return fullCase
def delFullBlack_one(case):
    temp = os.listdir(case+'GT/')
    gts = [case+'GT/'+x for x in temp]
    imgs  = [case+'Images/'+x for x in temp]

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
def delFullBlack():
    cases = loadFullCase()
    for item in cases:
        case = PATH+item+'/'
        delFullBlack_one(case)
# delFullBlack()

###对原数据改名，方便数据增强表示###
def zero(path):
    def reName(data):
        s = data.split('/')
        ss = s[-1].split('.')
        sss = ss[0].zfill(4) + '.bmp'
        s[-1] = sss
        name = '/'.join(s)
        return name
    dir = os.listdir(path)
    mix = []
    for i in dir:
        item_dir = os.listdir(path+i+'/')
        for j in item_dir:
            j_name = path+i+'/'+j
            mix.append(j_name)
    for item in mix:
        rename = reName(item)
        os.rename(item,rename)
def zero_case(path):
    dir = os.listdir(path)
    for case in dir:
        case_name = path+case+'/'
        zero(case_name)
# zero_case(PATH)
# temp.txt 如果原来有，要删除掉，再重新生成
file = './temp.txt'
def getTxt(path,file):
    def data2txt(path, file):
        fp = open(file, 'a')
        dir = os.listdir(path)
        for case in dir:
            case_name = path + case + '/'
            case_dir = os.listdir(case_name)
            for item in case_dir:
                item_name = case_name + item
                fp.write(item_name + '\n')
        fp.close()
    dir = os.listdir(path)
    for item in dir:
        item_name = path+item+'/'
        data2txt(item_name,file)
# getTxt(PATH,file)
def txt2data(file):
    data = []
    fp = open(file, 'r')
    while 1:
        line = fp.readline().rstrip('\n')
        data.append(line)
        if not line:
            break
    data.pop()
    return data
data = txt2data(file)

def reName(name):
    s = name.split('/')
    ss = s[-1].split('.')
    sss = str(int(ss[0])+6000) + '.bmp'
    s[-1] = sss
    name = '/'.join(s)
    return name
def flippedHorizontally(data):
    for item in data:
        image = cv2.imread(item,0)
        temp = cv2.flip(image,1)
        name = reName(item)
        cv2.imwrite(name,temp)
def rotation(data):
    for item in data:
        image = cv2.imread(item,0)
        row,col = image.shape
        temp = cv2.getRotationMatrix2D((col/2,row/2),45,1)
        dst = cv2.warpAffine(image,temp,(col,row))
        name = reName(item)
        cv2.imwrite(name,dst)
def cropScale(data):
    for item in data:
        image = cv2.imread(item,0)
        image = image[40:230,25:255]
        image = cv2.resize(image,(248,248))
        name = reName(item)
        cv2.imwrite(name,image)
def brighter(data):
    for item in data:
        image = cv2.imread(item,0)
        image = np.uint8(np.clip((cv2.add(1*image,30)), 0, 255))
        name = reName(item)
        cv2.imwrite(name, image)
def contrast(data):
    for item in data:
        image = cv2.imread(item, 0)
        image = np.uint8(np.clip((cv2.add(1.5 * image, 0)), 0, 255))
        name = reName(item)
        cv2.imwrite(name,image)
def gammaTransform(data):
    for item in data:
        s = item.split('/')
        image = cv2.imread(item,0)
        if s[-2] == 'Images':
            img = image/255.0
            gamma = 0.6
            out = np.power(img,gamma)*255.0
        else:
            out = image
        name = reName(item)
        cv2.imwrite(name,out)

# flippedHorizontally(data) #1
# rotation(data) #2
# cropScale(data) #3
# brighter(data) #4
# contrast(data) #5
# gammaTransform(data) #6


###统计切片情况，创建0-1标签（用于挑选测试数据）###
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
            labels.append((gts[i],1))
        else:
            labels.append((gts[i],0))
    return labels
def numOfTumor(path):
    a = os.listdir(path)
    nums =[]
    for item in a:
        x, y = getData(path + item)
        labels = getLabel(y)

        t = [y for x, y in labels]
        t = np.array(t)
        tumor_num = np.sum(t == 1)
        kidney_num = len(t) - tumor_num
        nums.append((item,'tumor_num：' + str(tumor_num), 'kidney_num(no tumor)：' + str(kidney_num)))
    if not os.path.exists(dir+'/numOfTumor.txt'):
        f = open(dir+'/numOfTumor.txt', 'w')
        for line in nums:
            f.write(line[0] + '\t' + line[1] +'\t' + line[2] + '\n')
        f.close()
    else:
        print('exist')
# 在进行数据增强之前，统计切片情况（分析肿瘤数目）
# numOfTumor(PATH)

def create(path):
    '''
    该函数生成每个案例的标签情况。每个案例下，多了一个txt文件，保存标签情况
    :param path: 所有案例所在的目录
    :return: 无
    '''
    a = os.listdir(path)
    for item in a:
        x,y = getData(path+item)
        labels = getLabel(y)

        filename = item+'.txt'
        casePath = path+item+'/'
        if not os.path.exists(casePath+filename):
            f = open(casePath+filename,'w')
            f.close()
        fp = open(casePath+filename,'w')
        for line in labels:
            fp.write(line[0]+'\t'+str(line[1])+'\n')
        fp.close()
def read(path,case):
    '''
    #read(PATH,'case_00018') #该函数测试从文本读取数据
    该函数读取每个案例的txt文档
    :param path: 所有案例所在的路径
    :param case: 案例编号
    :return: 每张切片是否有肿瘤的列表
    '''
    casePath = path+case+'/'
    filename = casePath+case+'.txt'
    fp = open(filename,'r')
    labels = []
    while 1:
        line = fp.readline().rstrip("\n")
        label = list(line.split('\t'))
        labels.append(label)
        if not line:
            break
    labels.pop()
    return labels
#create(path=PATH) #该函数创建0-1标签标记

###划分数据集（先做数据增强，再划分数据集）###
def randomDiv(path,size):
    # 该函数对数据集进行划分，随机选取训练集、测试集
    nameSets = os.listdir(path)
    nameSets = [str(path) + name for name in nameSets]

    lenOfSets = len(nameSets)
    trainSize = int(size[0]*lenOfSets)
    validationSize = int(size[1]*lenOfSets)

    trainDataset = random.sample(nameSets,trainSize)
    leaveDataset = set(nameSets) - set(trainDataset)
    validationDataset = random.sample(leaveDataset,validationSize)
    testDataset = set(leaveDataset) - set(validationDataset)

    return trainDataset,validationDataset,list(testDataset)
def generateSets(dict,dir):
    '''
    该函数生成训练集数据文件、验证集数据文件、测试集数据文件
    :param dict: 数据集字典
    :param dir: 数据集所在的父目录：'F:/KiTs_dataset/'
    :return: 无
    '''
    for key in dict.keys():
        filename = key
        if not os.path.exists(dir+filename):
            f = open(dir+filename,'w')
            f.close()
        fp = open(dir+filename,'w')
        for line in dict[key]:
            fp.write(line+'\n')
        fp.close()
trainData,validationData,testData = randomDiv(PATH,(0.6,0.2,0.2))
dict = {}
dict['trainData.txt'] = trainData
dict['validationData.txt'] = validationData
dict['testData.txt'] = testData
# generateSets(dict,dir)

###挑选测试数据###
def generateData(path):
    '''
    该函数得到训练数据，保留所有肿瘤的切片，无肿瘤的切片随机选取
    随机选取的无肿瘤切片数目和有肿瘤切片数目尽量相同
    存在肿瘤切片多，无肿瘤切片少的情况，此时取所有切片
    :param path:
    :return:
    '''
    cases = os.listdir(path)
    for case in cases:
        casePath = path + case + '/'
        one = read(path,case)
        data0 = []
        data1 = []
        for item in one:
            if item[1] == '1':
                data1.append(item[0])
            else:
                data0.append(item[0])

        if len(data0) <= len(data1):
            data = data0+data1
        else:
            data = random.sample(data0,len(data1))
            data = data1+data
        random.shuffle(data)

        filename = casePath+'selectData.txt'
        if not os.path.exists(filename):
            f = open(filename, 'w')
            f.close()
        fp = open(filename, 'w')
        for line in data:
            fp.write(line + '\n')
        fp.close()
#generateData(PATH)



# def loadFullCase1(path=PATH):
#     # 得到所有案例名称
#     fullCase = os.listdir(path)
#     return [path+x for x in fullCase]
# allCase = loadFullCase1('F:/Datasets_IMAGE/KITS2020/DATA/')
# def oneSelect(dirPath,slice_num):
#     imgPath = dirPath+'/Images/'
#     file = dirPath+'/data.txt'
#     file = file.replace('DATA','TEST')
#     data = os.listdir(imgPath)
#     if len(data) < slice_num:
#         diff = (slice_num-len(data))//2+1
#         for i in range(1,diff):
#             data.insert(0,data[0])
#         for i in range(diff):
#             data.append(data[-1])
#         data = data[:slice_num]
#     else:
#         mid = len(data)//2
#         data = data[mid-slice_num//2:mid+slice_num//2]
#     data = [str(0)+x for x in data]
#     fp = open(file, 'w')
#     for item in data:
#         fp.write(item + '\n')
#     fp.close()
# for x in allCase:
#     pass
    # oneDel(x)
    # oneSelect(x,64)