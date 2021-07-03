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
        self.alpha = 0.1
        self.gamma = 0.9
        self.lr = 0.01
        self.action_dim = action_dim
        self.iter_step = 0
        self.TARGET_UPDATE_STEP = 100
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


    def act(self, obs):
        # 不能直接用预测出来的Q值来选择动作，应当剔除掉做不到的动作，在可以做到的动作中选择最优的
            # 否则它会一直选Q值最大但是做不到的动作
            # 1.判断当前状态下哪个动作可行，哪些动作不可行
            # 2.将不可行的动作的Q值设为负值，比如-10
            # 3.然后依据Q值选择最佳动作
            # 4.即使随机选择也要把不可行的排除在外

        
        if random.random() < self.epsilon:
            actions_value = self.eval_net(obs)
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
        iterate and train by Q-Learining
        '''
        self.iter_step = self.iter_step % 1000 + 1
        if self.iter_step % self.TARGET_UPDATE_STEP == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict()) # update target net
            # print("---------------- Update target net")

        reward = 0
        for i in range(len(obs_batch)):   # for i in range(batch_size)
            # print("obs_batch:",obs_batch)
            obs = torch.Tensor(obs_batch[i][self.NO])
            action = action_batch[i][self.NO]   # 怎么强化对应的action呢
            
            obs_next = torch.Tensor(obs_next_batch[i][self.NO])
            done_i = done[i][self.NO]
            # 直接用环境返回的reward相加来计算reward
            r = reward_batch[i][self.NO]
            '''
            r = -1
            # 根据done简单计算reward
            if(done_i):
                r += 10      # agent_i到达终点时，r=10
            if(done[i]["__all__"]):
                r += 10     # 所有agent到达终点时，再加10
            '''
            reward += r   # reward

            # print("obs:",obs)
            # print("action:",action)
            # TODO 不能只更新action对应的loss，应该更新每个q值的loss
            # action对应的q值，用q_target来更新，其他的用它自己或加上-0.1来更新
            q_pre = self.eval_net(obs)
            q_tar = q_pre.clone().detach()

            q_eval = q_pre[action]
            
            # q_target = q_eval.clone()
            # print("q_eval:",q_eval)
            q_next = self.target_net(obs_next).detach()
            # print("q_next:",q_next)
            
            # q_target = r + self.gamma * q_next.max()
            # TODO 下面这个公式才是对的
            q_target = q_eval + self.alpha * (r + self.gamma * q_next.max() - q_eval)
            q_tar[action] = q_target
            # q_target[action] = q_
            # print("q_next, r:", q_next, r)
            # print("action, q_", action, q_)
            # print("q_eval, q_target:",q_eval, q_target)

            loss = self.loss_func(q_pre,q_tar)
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
        with open(save_path+'RLagent_'+str(self.NO)+".pkl", 'wb') as f:
                torch.save(self.target_net, f)

        print("Model %d Saved!" % self.NO)

    def show(self,show_loss=True,show_acc=True):
        x_loss = range(len(self.loss_list))
        x_acc = range(len(self.acc_list))
        y_loss = self.loss_list
        y_acc = self.acc_list

        if show_loss:
            plt.subplot(3, 1, 1)
            plt.plot(x_loss, y_loss, '.-')
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
        plt.savefig("accuracy_loss.jpg")



# print("#########")
