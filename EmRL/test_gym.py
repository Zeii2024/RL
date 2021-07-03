import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import gym
from Agent_for_gym import Agent_gym
from memory import Memory
import time

# Hyper Parameters
BATCH_SIZE = 32
epochs = 650
MEMORY_CAPACITY = 500  # 这个参数挺重要的

env = gym.make('CartPole-v0')
env = env.unwrapped
N_ACTIONS = env.action_space.n
N_STATES = env.observation_space.shape[0]

agent = Agent_gym(0,1,N_STATES,10,N_ACTIONS)
memory = Memory(MEMORY_CAPACITY,BATCH_SIZE)


def train():
    print('\nCollecting experience...')
    for i_episode in range(epochs):
        s = env.reset()
        
        s = torch.Tensor(s)
        # print("s: ",s)
        if(i_episode % 100 == 0):
            print("episode:",i_episode)
        while True:
            env.render()
            a = agent.act(s)
            # take action
            s_,r,done,info = env.step(a)
            s_ = torch.Tensor(s_)
            # print("s:",s)
            # print("s_:",s_)

            # modify the reward
            x,x_dot,theta,theta_dot = s_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            r = r1 + r2
            # print("reward:",r)
            
            memory.store_memory(s,a,r,s_,done)
            if memory.memory_counter >= MEMORY_CAPACITY:
                obs,action,rewards,obs_next,done = memory.get_replay_batch()
                # print("obs:",obs)
                # print("action:",action)
                agent.step(obs,action,rewards,obs_next,done)
            if done:
                break
            s = s_
    
    save_path = 'D:/桌面/My_TTP/EmRL/save/'
    agent.save_model(save_path)


def test():
    # load model
    load_path = 'D:/桌面/My_TTP/EmRL/save/'
    # agent.load_model(load_path)

    for i in range(2):
        print("---------------------")
        print("---------test episode: ", i)
        print("---------------------")
        s = env.reset()
        s = torch.Tensor(s)

        a = agent.act(s)
        s_,r,done,_ = env.step(a)
        s_ = torch.Tensor(s_)
        step = 0
        while not done:
            env.render()
            step += 1

            '''
            不同的是，gym每一步都会有一个奖励，可以单独纠正每一个状态下的动作
            而TTP只在终点处设置奖励
            '''
            x,x_dot,theta,theta_dot = s_
            r1 = (env.x_threshold - abs(x)) / env.x_threshold - 0.8
            r2 = (env.theta_threshold_radians - abs(theta)) / env.theta_threshold_radians - 0.5
            r = r1 + r2

            print("step: ", step, end=' ')
            print("reward: ", float(r))

            s = s_
            a = agent.act(s)
            s_,r,done,info = env.step(a)
            s_ = torch.Tensor(s_)

            time.sleep(0.01)
            if step == 500:
                break
 
        print(i," done!")



train()  
#time.sleep(2)
# test()

agent.show()   

