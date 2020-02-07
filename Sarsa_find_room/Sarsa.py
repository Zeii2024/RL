# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:51:23 2019

@author: Terry
using python 3.7
"""
import numpy as np
import pandas as pd
import pickle
import time

STATES = [0,1,2,3,4,5]
ACTIONS = [0,1,2,3,4,5]
N_states = 6
N_actions = 6
ALPHA = 0.1       #learning rate
EPSILON = 0.9     #epsilon_greedy
GAMMA = 0.9       #decay factor
MAX_EPISODES = 16

R_table = pd.DataFrame([[-1, -1, -1, -1, 0, -1],
                        [-1, -1, -1, 0, -1, 10],
                        [-1, -1, -1, 0, -1, -1],
                        [-1,  0,  0, -1, 0, -1],
                        [0,  -1, -1, 0, -1, 10],
                        [-1,  0, -1, -1, 0, 10]])

#创建q_table，并初始化为全0
def create_q_table(states, actions):
    q_table = pd.DataFrame(np.zeros((states, actions)), index = STATES,
                columns = ACTIONS)
    return q_table

#返回状态S下可以选择的actions
def pro_action(S, R_table):  
    a = R_table.loc[S]
    a_index = list(range(6))
    for i in a.index:
        if a[i] == -1:
            a_index.remove(i)
    return a_index

#状态S下，依据q_table选择action
def choose_action(S, q_table):
    state_actions = pro_action(S, R_table) #S行可选的actions
    q_actions = q_table.iloc[S, :]  #S行所有的actioons
    
    #90%概率选择当前最优，10%概率随机选择
    if (np.random.uniform() > EPSILON) or ((q_actions == 0).all()):
        action_name = np.random.choice(state_actions)
    else:
        action_name = q_actions[state_actions].idxmax()  #q_actions是一个一维向量
    return action_name

#环境，即房间结构图        
def env():
    print(2, '-'*5, 3, '-'*5, 4, '-'*5, 0, end = '\n')
    print(' '*7, '|', ' '*5, '|', end = '\n')
    print(' '*7, 1, '-'*5, '\033[33m5\033[0m')
    
#print(\033[显示方式;前景色;背景色m输出内容\033[0m)
#更新环境，打印找门路径
def env_update(S, A, episode_num, step_counter):
    if S != 5:
        time.sleep(0.5)
        print('--', A, end = '')
    else:
        time.sleep(0.5)
        print(' ---\033[33m%s\033[0m'%S)  #终点打印为红色
        time.sleep(0.3)
        print('Episode %s used steps: %s'%(episode_num + 1, step_counter))

#依据S,A，得到S_ 和 Reward
def get_env_feedback(S, A):
    #根据S,A返回S_和Reward
    Reward = R_table.loc[S, A]
    S_next = A
    return S_next, Reward

#Training       
def rl():    
    q_table = create_q_table(N_states, N_actions)
    env()
    for i in range(MAX_EPISODES):
        step_counter = 0
        S = np.random.choice(range(5))  #随机选择初始状态，不包括终点5
        terminated = False   #终止标记
        A = choose_action(S, q_table)    #选择action
        print('\033[35m%s\033[0m'%S, end = '')  #初始状态为紫色
        #print(q_table)
        while not terminated:
            
            S_next, Reward = get_env_feedback(S, A)   #得到S_next和Reward
            A_next = choose_action(S_next, q_table)
            
            q_predict = q_table.iloc[S, A]  #取当前Q(S,A)的值
            
            if (S_next != 5):
                q_target = Reward + GAMMA * (q_table.loc[S_next, A_next])#更新函数与QL不同
                '''
                Sarsa和QL的区别在于，QL是在模型中探索动作a，得到r和s'，但下一周期实际执行的动作a不一定是这个a，而是重新选择
                而Sarsa，在模型中探索动作a，则下一步动作就是动作a，即a = a_next
                在下一周期的探索中，sarsa的动作a是根据上一周期的反馈来确定的，因此在每一步的探索中，sarsa要比QL更谨慎
                很多时候sarsa效果要比QL好一些
                '''
            else:
                q_target = Reward    #没有走到状态5，所以这里单独更新下Q(5,5)
                q_table.loc[S_next, A] += ALPHA * (q_target - q_predict)
                terminated = True
            #每到达一次终点，更新一次Q_table， ALPHA是learning rate，即更新幅度
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)
            S = S_next
            #time.sleep(0.5)
            step_counter += 1
            env_update(S, A, i, step_counter) #更新环境
            A = A_next   #直接将A_next作为下一个动作，Q_learning下一步的A要根据Q重新选择

        time.sleep(0.5)  
             
    return q_table
       


if __name__ == '__main__':
    Q_table = rl()
    print('Brain:\n', Q_table)
    #with open('Sarsa_find_room5.pkl', 'wb') as f:
        #pickle.dump(Q_table, f)


