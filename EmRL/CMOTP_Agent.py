"""

2020-8-10
author @Terry
"""



import torch.nn as nn
import torch
import random
from collections import deque

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
        self.epsilon = 0.9
        self.alpha = 0.2  ####
        self.gamma = 0.9
        self.lr = 0.01
        self.action_dim = action_dim
        self.iter_step = 0
        self.TARGET_UPDATE_STEP = 500   ####
        self.num_of_agents = num_of_agents

        self.loss_list = deque(maxlen=5000)  # show the loss
        self.acc_list = deque(maxlen=5000)  # show the acc

        # self.main_enet = Main_Enet(input_dim,emb_dim,hiden_dim)
        # self.sub_enet = Sub_Enet(input_dim,emb_dim,hiden_dim)
        self.emb_net = Embed(self.num_of_agents, self.NO)
        self.eval_net = RL_net(emb_dim, action_dim,hiden_dim)
        self.target_net = RL_net(emb_dim,action_dim,hiden_dim)
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(),lr=self.lr)
        self.loss_func = nn.MSELoss(reduction='none')
    '''
    def loss_func(self, pre, tar):
        dim_pre = pre.shape()
        dim_tar = tar.shape()
        if dim_pre is not dim_tar:
            print("the dim of pre and tar is NOT same!")
            return TypeError
        loss = torch.tensor([0]*dim_pre)
    '''
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
        # 溢出
        if self.iter_step < 10000:
            self.iter_step += 1
        
        if self.iter_step % self.TARGET_UPDATE_STEP == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict()) # update target net
            if self.epsilon < 0.9:
                self.epsilon += 0.002
            # print(" Update target net")

        reward = 0
        for i in range(len(obs_batch)):   # for i in range(batch_size)
            # print("obs_batch:",obs_batch)
            obs = torch.Tensor(obs_batch[i][self.NO])
            action = action_batch[i][self.NO]   # 怎么强化对应的action呢
            
            obs_next = torch.Tensor(obs_next_batch[i][self.NO])
            # done_i = done[i][self.NO]
            # 直接用环境返回的reward相加来计算reward
            r = reward_batch[i][self.NO]
            '''
            r = 0
            # 根据done简单计算reward
            if(done_i):
                r += 10      # agent_i到达终点时，r=10
            if(done[i]["__all__"]):
                r += 10     # 所有agent到达终点时，再加10
            '''
            # reward += r   # reward

            # print("obs:",obs)
            # print("action:",action)
            # TODO 不能只更新action对应的loss，应该更新每个q值的loss
            # action对应的q值，用q_target来更新，其他的用它自己或加上-0.1来更新
            q_pre = self.eval_net(obs)
            # print("q_pre:", q_pre)
            q_tar = q_pre.clone().detach()
            # q_tar = torch.tensor(q_pre.detach())
            
            q_eval = q_pre[action]
            
            q_next = self.target_net(obs_next).detach()
            # print("q_next:",q_next)
            
            '''
            Q不取负值
            '''
            # q_target = r + self.gamma * q_next.max()
            # TODO 下面这个公式才是对的
            q_target = q_eval + self.alpha * (r + self.gamma * q_next.max() - q_eval)
            q_tar[action] = q_target
            # print("q_tar:", q_tar)
            # print("q_target: ", q_target)
            '''
            # 将q_target取非负
            if q_target > q_eval and q_target < 0:
                q_target = torch.Tensor([0.0])
            '''   
            # q_target[action] = q_
            # print("q_next, r:", q_next, r)
            # print("action, q_", action, q_)
            # print("q_eval, q_target:",q_eval, q_target)
            # loss 在更新时，只更新对应动作的值，没有选择的动作不更新Q值
            loss = self.loss_func(q_pre, q_tar)
            
            # print("****loss:", loss)
            # acc计算不对
            acc = np.abs(q_target.detach().numpy() -  \
             q_eval.detach().numpy()) / np.abs(q_target.detach().numpy())
            
            self.loss_list.append(loss)
            self.acc_list.append(acc)
            self.optimizer.zero_grad()
            loss.backward(torch.ones_like(q_pre))
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
        with open(save_path+'CMOTP_Agent_seq_'+str(self.NO)+"_eval.pkl", 'wb') as f1:
                torch.save(self.eval_net, f1)
        with open(save_path+'CMOTP_Agent_seq_'+str(self.NO)+"_target.pkl", 'wb') as f2:
                torch.save(self.target_net, f2)

        print("Model %d Saved!" % self.NO)

    def load_model(self, load_path):
        '''
        load model from pickle file
        '''
        with open(load_path+'CMOTP_Agent_seq_'+str(self.NO)+"_eval.pkl", 'rb') as f1:
            self.eval_net = torch.load(f1)
        with open(load_path+'CMOTP_Agent_seq_'+str(self.NO)+"_target.pkl", 'rb') as f2:
            self.target_net = torch.load(f2)
        
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
