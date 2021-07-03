import torch
import torch.nn as nn
import numpy as np
from normalize_obs import Normal_local_obs

class Main_Enet(torch.nn.Module):
    '''
    1.将rail_obs从16*1*5*5压缩到4*5*5时：
    Main Embedding Net
    input: obs (shape = 304 * 1) 304 = (5*5*4)*3 + 4
    output: obs_embedding (shape = 16 * 1)
    hiden_dim: 108

    parms: 
    input_dim: dimension of input 
    out_dim: dimension of output 
    hiden_dim: 108

    attention: agent数量较少时，emb_main 16位，emb_sub 较少，差距会有些大
    当 agent数量在16个左右时，二者权重才差不多
    可以考虑不同情况emb_main的维度也不一样，比如8位等。

    2.rail_obs的维度不压缩，保持16*5*5时：
    Main Embedding Net
    input: obs (shape = 604 * 1) 604 = (5*5*16)*3 + 4
    output: obs_embedding (shape = 16 * 1)
    hiden_dim: 151

    parms: 
    input_dim: dimension of input 
    out_dim: dimension of output 
    hiden_dim: 108
    '''
    def __init__(self,input_dim,out_dim,hiden_dim):
        super(Main_Enet,self).__init__()
        
        self.fc1 = nn.Linear(input_dim, hiden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hiden_dim, out_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x

class Sub_Enet(torch.nn.Module):
    '''
    Sub Embedding Net
    input: obs (shape = 304 * 1) 304 = (5*5*4)*3 + 4   #604
    output: obs_embedding (shape = 1 * 1)

    parms: 
    input_dim: dimension of input 
    out_dim: dimension of output 
    hiden_dim: 108   #151
    '''
    def __init__(self,input_dim,out_dim,hiden_dim):
        super(Sub_Enet, self).__init__()
         
        self.sub_fc1 = nn.Linear(input_dim, hiden_dim)
        self.sub_relu = nn.ReLU()
        self.sub_fc2 = nn.Linear(hiden_dim, out_dim)

    def forward(self, x):
        x = self.sub_fc1(x)
        x = self.sub_relu(x)
        x = self.sub_fc2(x)

        return x


# 把这个用上
class Rail_Enet(torch.nn.Module):
    '''
    loacal rail info to embedding obs
    input: local rail obs (shape = 400 = 16*5*5)
    output: rail_embedding (shape = 4 / 8 / 16 * 1)
    '''
    def __init__(self,input_dim,out_dim,hiden_dim):
        super(Rail_Enet,self).__init__()
        
        self.fc1 = nn.Linear(input_dim, hiden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hiden_dim, out_dim)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)

        return x


class Embed():
    '''
    Embed 放入到Agent里面了
    Embed的输入为env的obs
    输出单个的embedding
    把循环for i in range(num_of_agents)放在train里
    '''
    '''
    env_obs = env.step(actions)
    local_obs = format_local_obs(env_obs) : 304  # 604
    main_enet = Main_Enet(304,16,108)  # (604,16,151)
    x = torch.Tensor(local_obs[NO]) : 304
    main_emb = main_enet(x): 16
    sub_out = sub_emb_out(local_obs): 1 / dict
    oth_emb = concat_sub_emb(sub_out): n-1
    obs_emb = concat_main_sub_emb(main_emb,oth_emb): 16 + n - 1

    '''
    def __init__(self,num_of_agents,NO):
        self.num_of_agents = num_of_agents
        self.NO = NO
        self.emb_input_dim = 604  #304
        self.hiden_dim = 151  #108


    def sub_emb_out(self,local_obs):
        # 得加一个agent的编号  --> 加了：self.NO
        
        sub_e_dict = {}
        sub_emb = Sub_Enet(self.emb_input_dim,1,self.hiden_dim)
        for i in range(self.num_of_agents):
            if i is not self.NO:
                x = torch.Tensor(local_obs[i])
                emb_out = sub_emb(x)
                sub_e_dict.update({i:emb_out})

        return sub_e_dict

    def concat_sub_emb(self,sub_out):
        oth_emb = np.array([])
        for idx in sub_out:
            oth_emb = np.concatenate((oth_emb,sub_out[idx].detach().numpy()),axis=0)
        
        return oth_emb

    def concat_main_sub_emb(self,main_emb, oth_emb):
        if type(main_emb) == torch.Tensor:
            main_emb = main_emb.detach().numpy()
        obs_emb = np.concatenate((main_emb,oth_emb),axis=0)
        
        return obs_emb

    def local_obs_to_emb(self,obs):
        '''
        return: obs_emb   15+N * 1
        '''
        normal_obs = Normal_local_obs(obs,self.num_of_agents)
        local_obs = normal_obs.format_local_obs()
        main_enet = Main_Enet(self.emb_input_dim,16,self.hiden_dim)
        x = torch.Tensor(local_obs[self.NO]) 
        main_emb = main_enet(x)
        sub_out = self.sub_emb_out(local_obs)
        oth_emb = self.concat_sub_emb(sub_out)
        obs_emb = self.concat_main_sub_emb(main_emb,oth_emb)

        return obs_emb