"""

2020-8-10
author @Terry
"""
'''
一个sub_net/或者公式: obs_B --> o_b
一个main_net: obs_A + o_b  --> Q/action 
'''


import torch.nn as nn
import torch
import random

import numpy as np
import matplotlib.pyplot as plt
from Embed import Embed



class RL_net(torch.nn.Module):
    '''
    input: embedding of obs
    output: values of actions
    '''
    def __init__(self,in_feature,out_feature,hiden_feature=16):  # hiden_dim = 16
        super(RL_net,self).__init__()
        self.fc1 = nn.Linear(in_feature, hiden_feature)
        self.fc1.weight.data.normal_(0,0.1)  # initialize
        self.tanh = nn.Tanh()
        self.fc2 = nn.Linear(hiden_feature,out_feature)
        self.fc2.weight.data.normal_(0,0.1)  # initialize

    def forward(self,x):
        x = self.fc1(x)
        x = self.tanh(x)
        x = self.fc2(x)

        return x
        

class Agent():
    '''
    Double-DQN
    @params:
    NO: the No. of agents
    num_of_agents: the number of agents
    emb_dim: Agent net input dim = 15 + N
    hiden_dim: Agent net hiden dim
    action_dim: Agent net output dim = number of actions
    '''
    def __init__(self, NO, num_of_agents, emb_dim, hiden_dim,action_dim=5):
        self.NO = NO
        self.epsilon = 0.5
        self.alpha = 0.1
        self.gamma = 0.9
        self.lr = 0.01
        self.action_dim = action_dim
        self.iter_step = 0
        self.TARGET_UPDATE_STEP = 100
        self.num_of_agents = num_of_agents

        self.loss_list = []  # show the loss
        self.acc_list = []  # show the acc

        # self.main_enet = Main_Enet(input_dim,emb_dim,hiden_dim)
        # self.sub_enet = Sub_Enet(input_dim,emb_dim,hiden_dim)
        self.emb_net = Embed(self.num_of_agents, self.NO)
        self.eval_net = RL_net(emb_dim, action_dim,hiden_dim)
        self.target_net = RL_net(emb_dim,action_dim,hiden_dim)
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(),lr=self.lr)
        self.loss_func = nn.MSELoss()


    def act(self, obs):
        if random.random() < self.epsilon:
            actions_value = self.eval_net(obs)
            
            # TODO action是取Q值最大的序号，能不能直接取Q值，然后取整？？
            action = torch.max(actions_value,-1)[1].data.numpy()  # max actions value
            # action = check_actions(action)
        else:
            action = random.choice(range(self.action_dim))
        return action

    def check_actions(self, action):
        '''
        TODO   make sure the actions are leagel
        '''
        return action

    def step(self,obs_batch,action_batch,reward_batch,obs_next_batch,done):
        '''
        iterate and train by Q-Learning
        '''
        self.iter_step += 1
        if self.iter_step % self.TARGET_UPDATE_STEP == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict()) # update target net
            if self.epsilon < 0.9:
                self.epsilon += 0.002
            print("---------------- Update target net")

        reward = 0
        # 从batch里取出此agent对应的数据，再组成一个batch 并转化成tensor
        obs_b = []
        action_b = []
        reward_b = []
        obs_next_b = []
        done_b = []
 
        for i in range(len(obs_batch)):
            obs_b.append(obs_batch[i][self.NO])
            action_b.append(action_batch[i][self.NO])
            reward_b.append(reward_batch[i][self.NO])
            obs_next_b.append(obs_next_batch[i][self.NO])
            done_b.append(done[i][self.NO])
        
        # 转化成tensor
        obs_b = torch.FloatTensor(obs_b)
        action_b = torch.LongTensor(action_b)
        reward_b = torch.FloatTensor(reward_b)
        obs_next_b = torch.FloatTensor(obs_next_b)

        # 根据动作选出q_eval值
        q_eval = self.eval_net(obs_b).gather(1,obs_b)
        q_next = self.target_net(obs_next_b).detach()
        q_target = reward_b + self.gamma*q_next.max(1)[0]

        loss = self.loss_func(q_eval, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # print("step successd")
        return reward

    def emb(self,obs):
        obs_emb = self.emb_net.local_obs_to_emb(obs)
        obs_emb = torch.Tensor(obs_emb)
        return obs_emb

    def save_model(self,save_path):
        '''
        save model to pickle
        '''
        with open(save_path+'CMOTP_Agent_2_'+str(self.NO)+"_eval.pkl", 'wb') as f:
                torch.save(self.eval_net, f)
        with open(save_path+'CMOTP_Agent_2_'+str(self.NO)+"_target.pkl", 'wb') as f:
                torch.save(self.target_net, f)

        print("Model %d Saved!" % self.NO)

    def load_model(self, load_path):
        '''
        load model from pickle file
        '''
        with open(load_path+'CMOTP_Agent_2_'+str(self.NO)+"_eval.pkl", 'rb') as f:
            self.eval_net = torch.load(f)
        with open(load_path+'CMOTP_Agent_2_'+str(self.NO)+"_target.pkl", 'rb') as f:
            self.target_net = torch.load(f)
        
        print("Model %d loaded!" % self.NO)

    def show(self,show_loss=True,show_acc=True):
        x_loss = range(len(self.loss_list))
        x_acc = range(len(self.acc_list))
        y_loss = self.loss_list
        y_acc = self.acc_list

        if show_loss:
            plt.subplot(3, 1, 1)
            plt.plot(x_loss, y_loss, '-')
            plt.title('Test loss vs. epoches')
            plt.ylabel('Test loss')

            # show last 1000 loss
            if len(self.loss_list) > 1000:
                plt.subplot(3,1,2)
                y_loss_last = self.loss_list[len(self.loss_list)-1000 : len(self.loss_list)]
                x_loss_last = range(len(y_loss_last))
                plt.plot(x_loss_last, y_loss_last,'-')
                plt.xlabel('Last 1000 loss vs. epochs')
                plt.ylabel('last 1000 loss')
            else:
                print("length of loss_list is less than 1000!")

        if show_acc:
            plt.subplot(3, 1, 3)
            plt.plot(x_acc, y_acc, '.-')
            plt.xlabel('Test accuracy vs. epoches')
            plt.ylabel('Test accuracy')
        
        plt.show()
        plt.savefig("PSD_accuracy_loss.jpg")



# print("#########")
