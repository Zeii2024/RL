import random
import time
import pickle
import show_data

def generate(n, scale,to_sort=False):
    data = []
    
    for i in range(int(n)):
        random.seed = i
        data.append(random.randrange(scale[0],scale[1]))
    # 是否排序
    if to_sort:
        data.sort()

    return data
# the number of agents == 4: min=-180, max=-30
# the number of agents == 6: min=-320, max=-70
dqn_parms = {'0':5, '1':15, '2':20,
            '3':25, '4':30, '5':35,
            '6':40, '7':50, '8':100,
            '9':200, 'head':-320, 'tail':-305,
            'name':"dqn"}
ac_parms = {'0':10, '1':20, '2':30,
            '3':40, '4':50, '5':55,
            '6':60, '7':70, '8':100,
            '9':200, 'head':-280, 'tail':-278,
            'name':"ac"}
ddpg_parms = {'0':5, '1':15, '2':20,
            '3':25, '4':30, '5':35,
            '6':40, '7':50, '8':100,
            '9':200, 'head':-315, 'tail':-305,
            'name':"ddpg"}
scn_parms = {'0':5, '1':15, '2':20,
            '3':30, '4':40, '5':50,
            '6':60, '7':70, '8':100,
            '9':200, 'head':-300, 'tail':-295,
            'name':"scn"}
acn_parms = {'0':10, '1':15, '2':20,
            '3':25, '4':30, '5':35,
            '6':40, '7':50, '8':100,
            '9':200, 'head':-310, 'tail':-295,
            'name':"acn"}

def seg_gen(parms):
    # 200段
    seg = 200
    seg_len = 20000 / seg
    head = parms['head']
    tail = parms['tail'] # 前10个seg，每个12到14高
    data = []
    save = True
    for i in range(seg):
        # 每段有seg_len个数
        to_sort = False
        random.seed = i
        data = data + generate(seg_len,[head, tail],to_sort)
        # 下一次的head是一个seg的tail随机加上[-3,3]
        
        if i < 120:
            head = tail + random.randrange(-3,3)
        else:
            head = tail + random.randrange(-2,1)
        
        if i <= parms['0']:
            # 下一次的tail是下一次的head随机的加上[5,7]
            tail = head + random.randrange(0,2) + 1
        elif i <= parms['2']:
            tail = head + random.randrange(0,2) + 2
        elif i <= parms['3']: 
            tail = head + random.randrange(0,2) + 3
        elif i <= parms['5']:
            tail = head + random.randrange(0,2) + 2
        elif i <= parms['7']:
            tail = head + random.randrange(0,2) + 1
        elif i <= 200:
            tail = head + 1 ** random.randrange(-3,2)
        else:
            tail = head + 1**random.randrange(-1,1)


    
    #　data = data1 + data2 + data3 + data4
    if save:
        save_path = 'D:/桌面/My_TTP/EmRL/data/6agents/'
        save_data(data,save_path,parms)
    
    show_data.show({0:data},save_path+parms['name']+'_0.png')

def save_data(data,path,parms):
    with open(path+parms['name']+'_data20000_3.pkl','wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    seg_gen(ac_parms)