import matplotlib.pyplot as plt
import pickle
import res_data
import seaborn as sns
import pandas as pd
import numpy as np


def load_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)

    return data

def show(data:dict,save_path):
    for a in data.keys():
        x = range(len(data[a]))
        
        y = data[a]
        # y.sort()
        plt.plot(x,y)
        plt.title("episode rewards")
        plt.xlabel("episodes")
        plt.ylabel("rewards")

        plt.savefig(save_path)
        plt.show()

def sns_show():
    

    acn = False
    '''
    purple = 'ddpg_data20000_01.pkl' # --> dqn
    blue = 'dqn_data20000_0.pkl'    # --> acn
    orange = 'ac_data20000_01.pkl'   # --> ac
    green = 'ddpg_data20000_00.pkl'  # --> scn
    red = 'scn_data20000_01.pkl'     # --> ddpg
    '''

    # blue - orange - green - red - purple

    path1 = 'D:/桌面/My_TTP/EmRL/data/6agents/dqn_20000_1.pkl'   # blue
    path2 = 'D:/桌面/My_TTP/EmRL/data/6agents/ac_20000_1.pkl'    # orange
    path3 = 'D:/桌面/My_TTP/EmRL/data/6agents/ddpg_20000_1.pkl'  # green
    path4 = 'D:/桌面/My_TTP/EmRL/data/6agents/scn_20000_1.pkl'   # red
    path5 = 'D:/桌面/My_TTP/EmRL/data/6agents/acn_20000_1.pkl'   # purple
    
    with open(path1,'rb') as f1:
        data_dqn = pickle.load(f1)
        #print("len3:",len(data_dqn))
    with open(path2,'rb') as f2:
        data_ac = pickle.load(f2)
        #print("len3:",len(data_dqn))
    with open(path3,'rb') as f3:
        data_ddpg = pickle.load(f3)
        #print("len3:",len(data_dqn))
    with open(path4,'rb') as f4:
        data_scn = pickle.load(f4)
        #print("len3:",len(data_dqn))
    with open(path5,'rb') as f5:
        data_acn = pickle.load(f5)
        #print("len3:",len(data_dqn))
    if acn:
        data_list = data_dqn + data_ac + data_ddpg + data_scn + data_acn
        class_list = ['DQN']*20000 + ['AC']*20000 +['DDPG']*20000 + ['SCN']*20000 + ['ACN']*20000
        # print(len(data_list))
        # x作为索引列
        x = [i for i in range(len(data_dqn))]
        x = x + x + x + x + x
        print(len(x))
    else:
        data_list = data_dqn + data_ac + data_ddpg + data_scn 
        class_list = ['DQN']*20000 + ['AC']*20000 +['DDPG']*20000 + ['SCN']*20000
        # print(len(data_list))
        # x作为索引列
        x = [i for i in range(len(data_dqn))]
        x = x + x + x + x
        print(len(x))
    # 两列数据
    data = pd.DataFrame({'episode': np.array(x),
                        'rewards': np.array(data_list),
                        'class': np.array(class_list),
                        # 'class':np.array(['rewards_3','rewards_1'])
                        })
    # print("one")    
    # 转换格式
    data['episode'] = data['episode'].astype('float64')
    data['rewards'] = data['rewards'].astype('float64')
    # data['class'] = data['class'].astype('float64')
    # data['rewards_1'] = data['rewards_1'].astype('float64')

    plt.figure(dpi=200)
    # 设置样式
    # print("two")
    g = sns.lmplot(x="episode",y="rewards",data=data,
                    markers=['.','.','.','.',],
                    scatter_kws={'color':"white"},
                    order=15,
                    #x_estimator=np.mean,
                    #x_bins=50,
                    hue='class',
                    #x_ci='ci',
                    ci=100,
                    #n_boot=50,
                    #x_jitter=10.,
                    #y_jitter=10.,
                    )
    '''
    g = sns.regplot(x="episode",y=["rewards_3","rewards_1"],data=data,
                    marker=['.','.'],
                    # order=6,
                    # scatter_kws={'s': [10,10],'color':['white','green'],},     # 设置散点属性，参考plt.scatter
                    # line_kws={'linestyle':'-','color':'#c72e29'} # 设置线属性，参考 plt.plot
                    # y_jitter=[0.03,0.03]
                    )
    '''
    sns.set(style="whitegrid",font_scale=2)
    g.fig.set_size_inches(8,6)
    # 4 agents时，ylim=(-200,0)
    # 6 agents时，ylim=(-350,0)
    g.set(xlim=(0, 20000), ylim=(-330, -20))

    # plt.title("sns show test")
    plt.xlabel("Episodes",fontdict={'size':14})
    plt.ylabel("Mean Episode Rewards",fontdict={'size':14})
    plt.show()
    print("done")

def show_single(path):
    with open(path,'rb') as f:
        data = pickle.load(f)

    x = [i for i in range(len(data))]
    data = pd.DataFrame({'episode': np.array(x),
                        'rewards': np.array(data),
                        # 'class': np.array(class_list),
                        # 'class':np.array(['rewards_3','rewards_1'])
                        })
    data['episode'] = data['episode'].astype('float64')
    data['rewards'] = data['rewards'].astype('float64')

    plt.figure(dpi=200)
    # 设置样式
    g = sns.lmplot(x="episode",y="rewards",data=data,
                    markers=['.'],
                    scatter_kws={'color':"white"},
                    order=15, 
                    ci=100,
                    )
    sns.set(style="whitegrid",font_scale=2.5)
    g.fig.set_size_inches(8,6)
    g.set(xlim=(0, 20000), ylim=(-320, -20))

    # plt.title("sns show test")
    plt.xlabel("Episodes",fontdict={'size':14})
    plt.ylabel("Mean episode rewards",fontdict={'size':14})
    plt.show()
    print("done")



if __name__ == '__main__':
    path = 'D:/桌面/My_TTP/EmRL/data/6agents/scn_20000_1.pkl'
    pic_path = 'D:/桌面/My_TTP/EmRL/data/4agents/pic_scn_01.png'
    # data = load_data(path)
    # data2_v = res_data.generate(10000,[-180,-30])
    # data2 = {0:data}
    # show(data2,pic_path)

    #sns_show()
    show_single(path)
