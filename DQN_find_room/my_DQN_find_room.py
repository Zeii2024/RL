'''
author@ Terry
2019.11.4

using python 3.7
tensorflow 2.0.0
'''

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import layers # , models, optimizers
# from tensorflow.keras.optimizers import RMSprop
from collections import deque
import random
import time 

'''
'''
states = np.array([0, 1, 2, 3, 4, 5])
actions = np.array([0, 1, 2, 3, 4, 5])

# 输入的数据不能有负值
R_table = pd.DataFrame([[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 10],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 10],
                        [0, 0, 0, 0, 0, 10]])

class DeepQNetwork:
    def __init__(self, n_states, n_actions):
        # 初始化一些常量
        self.n_states = n_states
        self.n_actions = n_actions
        self.ALPHA = 0.1
        self.GAMMA = 0.8
        self.epsilon = 0.9
        self.batch_size = 20
        self.epsilon_increment = 0
        self.memory_size = 500

        self.step_counter = 0
        # 用双端队列来定义记忆空间，最大容量为500，容量满时会自动删除最早的记忆
        self.memory = deque(maxlen = self.memory_size)
        self.memory_counter = 0
        self.train_num = 0

        self.model = self.create_model()

        # 对状态s可选的动作进行预选
        self.pre_actions = [[4],[3,5],[3],[1,2,4],[0,3,5],[4,5]]
       
        # 记录cost变化过程，用于可视化输出
        # self.cost_his = []

    def create_model(self):
        """
        创建一个两层的神经网络，隐藏层32维
        """

        STATE_DIM, ACTION_DIM = 1, 6
        model = tf.keras.models.Sequential([
            layers.Dense(32, input_dim=STATE_DIM, activation='relu'),
            layers.Dense(ACTION_DIM, activation='linear')
            ])
        model.compile(loss='mean_squared_error',
                        optimizer = tf.keras.optimizers.Adam(0.001))
        print("create_model")
        return model

    # 将记忆存储在记忆空间
    def store_memory(self, s, a, r, s_next):

        self.memory.append((s, a, r, s_next))
        self.memory_counter += 1
        # print("store_memory")


    def choose_action(self, s):
        # epsilon-greedy,选择动作
        # 加入了对可选动作的限制
        if len(self.memory) < 100 : # and self.train_num < 3:
            action = np.random.choice(self.pre_actions[s])
            # print("random action = ", action)
            return action
        # 加入了对可选动作的限制
        if np.random.uniform() < self.epsilon :
            predict_actions = self.model.predict(np.array([s]))[0]
            # print("row_predict = ", predict_actions)
            for i in range(6):
                if i not in self.pre_actions[s]:
                    predict_actions[i] = 0
                # else:
                   # predict_actions[i] = np.abs(predict_actions[i])
            # print("predict_actions = ", predict_actions)
            action = np.argmax(predict_actions)
            # print("s = ", s)
            # print("action = ", action)
        else:
            action = np.random.choice(self.pre_actions[s])
        # print("state =============== ", s)
        # print("choose_action ======= ", action)
        return action

    def train(self, s):

        '''
        从memory中sample s和r，s_
        由s预测出Q
        由s_预测出Q_next
        根据更新公式得到Q
        将s, Q送入神经进行训练

        '''

        replay_batch = random.sample(self.memory, self.batch_size) # 从memory中抽取replay batch
        s_batch = np.array([replay[0] for replay in replay_batch]) # 从replay batch 中提取状态s --> s_batch
        
        # 问题在这里，S_next不能直接预测，也要进行筛选操作！！！！
        s_next_batch = np.array([replay[3] for replay in replay_batch])#从replay batch 中提取s_next --> s_next_batch
        # print("s_batch  = ", s_batch)
        # print("s_n_batch= ", s_next_batch)

        Q = self.model.predict(s_batch)  # 作为Q_predict
        Q_next = self.model.predict(s_next_batch)  # 作为 Q(s')
        # print("predict_Q = ", Q)
        for i in range(self.batch_size):
            for A in range(6):
                if A not in self.pre_actions[s_batch[i]]:
                    Q[i][A] = 0    # 这地方不能等于-100！！！！
                    Q_next[i][A] = 0
                else:
                    Q[i][A] =  self._relu(Q[i][A])     # 将负值的Q取0
                    Q_next[i][A] =  self._relu(Q_next[i][A])     # 将负值的Q取0
        
        # print("Q_next:", Q_next)

        for i, replay in enumerate(replay_batch):
            _, a, r, _ = replay         # 更新公式和Q-learning 一样
            Q[i][a] = Q[i][a] + self.ALPHA * (r + self.GAMMA * np.amax(Q_next[i]) - Q[i][a]) 
            # print("Q[{}][{}] = ".format(s, a), Q[i][a])
        # print("Q = ", Q)
        self.model.fit(s_batch, Q, verbose=0)
        # print("train done")

    # 把负值的Q变成0，杜绝出现负值
    def _relu(self, x):
        if x < 0: x = 0
        return x

# 打印环境 & 获得反馈feedback
class Enviroment:
    '''
    定义环境
    '''
    # 环境，即房间结构图，没有用到        
    def print_env(self):
        print(2, '-'*5, 3, '-'*5, 4, '-'*5, 0, end = '\n')
        print(' '*7, '|', ' '*5, '|', end = '\n')
        print(' '*7, 1, '-'*5, 5)   # '\033[33m5\033[0m'
        
    # print(\033[显示方式;前景色;背景色m输出内容\033[0m)
    # 更新环境，打印找门路径
    
    def env_update(self, S, A, episode_num, step_counter, end):
        if not end:
            print('--', A, end = '')
        else:
            # print(' ---\033[33m%s\033[0m'%S)  #终点打印为红色
            print(' ---', S)
            print('Episode %s used steps: %s'%(episode_num + 1, step_counter))
        
    # 依据S,A，得到S_next 和 Reward
    def get_env_feedback(self, S, A):
        # 根据S,A返回S_和Reward
        Reward = R_table.loc[S, A]
        S_next = A
        done = False
        if S == 5:
            done = True
        # print("get_feedback")
        return S_next, Reward, done

# 训练过程的测试函数
def test_print(s, episode_num):
    end = False
    steps = 0
    print(s, " -- ", end='')

    while not end:
        a = np.argmax(RL.model.predict(np.array([s]))[0])
        s_next, _, end = env.get_env_feedback(s, a)
        
        steps += 1
        env.env_update(s, a, episode_num, steps, end)
        s = s_next

    print("test_print")


def dqn():

    # step_counter = 0

    for i in range(episodes):
        s = np.random.choice(range(5)) # 随机初始状态
        print("s = ", s)
        episode_num = i

        # terminate = False
        # 往记忆池里放入3条新记录，然后取样训练一次 
        memory_num = 0
        RL.train_num = 0

        while True:
            a = RL.choose_action(s)
            s_next, r, done = env.get_env_feedback(s, a)

            RL.store_memory(s, a, r, s_next)
            # print("memory_num = ", len(RL.memory))
            # 把memory填满之后，再开始训练，每新迭代3次，训练一次
            if len(RL.memory) == 500 and memory_num > 10:
                RL.train(s)
                RL.train_num += 1
                # print("predict = ", RL.model.predict(np.array([s]))[0])
                print("episode_num = ", episode_num)
                break
            memory_num += 1


            if not done:
                s = s_next
            else:
                s = np.random.choice(range(5))
   
        # print("try_to_test_print")
        # test_print(s, episode_num)#输出测试



if __name__ == '__main__':
    episodes = 200   
    n_states = 6
    n_actions = 6
    RL = DeepQNetwork(n_states, n_actions)
    env = Enviroment()
    dqn()

    for s in range(6):
        print("s = ", s)
        Q = RL.model.predict(np.array([s]))[0]
        for i in range(6):
                if i not in RL.pre_actions[s]:
                    Q[i] = -100
                else:
                    Q[i] = np.abs(Q[i]) 
        acr = np.argmax(Q)
        print("a = ", acr)
        print(Q)
    # 保存模型
    # RL.model.save('DQN_find_room.h5')