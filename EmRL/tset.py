
import random
import pickle
import numpy as np 
import pandas as pd
from collections import deque

from ENV import ENV
from flatland.envs.agent_utils import EnvAgent
from flatland.envs.rail_env import RailEnv, RailEnvActions
from Embed import Main_Enet, Sub_Enet
from torch.autograd import Variable
import torch
'''
directions = {"North" : 0,
              "East"  : 1,
              "South" : 2,
              "West"  : 3}

'''
action_set = ['DO_NOTHING','MOVE_LEFT','MOVE_FORWARD','MOVE_RIGHT','STOP_MOVING']
# environment
env_params = {'width': 40,
                'height': 40,
                'max_num_cities': 3,
                'number_of_agents':3}
speed_ration_map = {1.: 0.,       # Fast passenger train
                    1. / 2.: 1.,  # Fast freight train
                    1. / 3.: 0.,  # Slow commuter train
                    1. / 4.: 0}  # Slow freight train


input_dim = env_params['number_of_agents'] + 4  #  输入为[x,y,d,s,Mi*N]
out_dim = len(action_set)         # 输出每个action的Q值

# initiate environment and agents
RE = ENV(env_params=env_params,speed_ration_map=speed_ration_map,obs_builder="local")
env = RE.env()

env_renderer = RE.env_renderer(env)
obs,info = env.reset()
env_renderer.reset()
agents = env.agents

def random_act():
    return np.random.choice(5,1)  # random choice 1 number from range(0,5)

def shorten_list(l:list):
    # 16位缩减到4位
    length = len(l)
    if(length == 16):
        return [float(l[0:4].count(1)),
                float(l[4:8].count(1)),
                float(l[8:12].count(1)),
                float(l[12:16].count(1))]

def expand_list(l):
    # 2位扩展到4位
    if(len(l)==2):
        l.extend([0.0,0.0])
    return l

def format_local_obs(obs):
    # agent a
    local_obs = {}
    for a in range(env.get_num_agents()):
        local_obs_a = []
        for row in range(len(obs[a][0])):
            for col in range(len(obs[a][0][row])):
                # l0_rail = shorten_list(list(obs[a][0][row][col]))
                l0_rail = list(obs[a][0][row][col])
                l0_target = expand_list(list(obs[a][1][row][col]))
                l0_oth_dir = list(obs[a][2][row][col])
                
                local_obs_a.extend(l0_rail)
                local_obs_a.extend(l0_target)
                local_obs_a.extend(l0_oth_dir)
                '''
                l1_rail.extend(l0_rail)
                l1_target.extend(l0_target)
            obs_rail_a.extend(l1_rail)
            obs_target_a.extend(l1_target)
        
        obs_rail.extend(obs_rail_a)
        obs_target.extend(obs_target_a)
        obs_oth_dir.extend(list(obs[a][2]))
        obs_dir.extend(list(obs[a][3]))
    
        obs_rail = np.array(obs_rail)
        obs_target = np.array(obs_target)
        obs_oth_dir = np.array(obs_oth_dir)
        
        obs_dir_new = obs_dir
        for i in range(4):
            obs_dir_new = np.concatenate((obs_dir_new,obs_dir), axis=0)
        obs_dir_new = np.array([[obs_dir_new]]) # 维度设为一样
        '''
       
        local_obs_a.extend(list(obs[a][3]))
        # local_obs_a = np.concatenate((obs_rail,obs_target,obs_oth_dir, obs_dir_new),axis=1) 
        local_obs.update({a:local_obs_a})
    
    return local_obs

def depart_obs(obs):
    '''
    obs_rail: 16*5*5
    obs_target: 2*5*5
    obs_oth_dir: 4*5*5 one-hot
    obs_dir: 4*1  one-hot
    '''
    obs_rail = {}
    obs_target = {}
    obs_oth_dir = {}
    obs_dir = {}
    for a in range(env.get_num_agents()):
        obs_rail.update({a:obs[a][0]})
        obs_target.update({a:obs[a][1]})
        obs_oth_dir.update({a:obs[a][2]})
        obs_dir.update({a:obs[a][3]})

    return obs_rail, obs_target, obs_oth_dir, obs_dir

def sub_emb_out(local_obs):
    # 得加一个agent的编号
    sub_e_dict = {}
    sub_emb = Sub_Enet(604,1,151)
    for i in range(env.get_num_agents()-1):
        x = torch.Tensor(local_obs[i+1])
        emb_out = sub_emb(x)
        sub_e_dict.update({i+1:emb_out})

    return sub_e_dict

def concat_sub_emb(sub_out):
    e_oth = np.array([])
    for idx in sub_out:
        e_oth = np.concatenate((e_oth,sub_out[idx].detach().numpy()),axis=0)
    return e_oth

def concat_main_sub_emb(emb_main, e_oth):
    if type(emb_main) == torch.Tensor:
        emb_main = emb_main.detach().numpy()
    e_obs = np.concatenate((emb_main,e_oth),axis=0)
    return e_obs

if __name__ == '__main__':
    actions = {}
    for a in range(env.get_num_agents()):
        action = random_act()[0]
        actions.update({a:action})

    obs, rewards, done, _ = env.step(actions)
    print("obs_builder:",RE.obs_builder)
   
    # print("obs[0]:", obs[0])
    print("obs[0][0]:",obs[0][0])
    local_obs = format_local_obs(obs)
    print("local_obs:", local_obs)
    print("nums of obs", len(local_obs[0]))
    main_emb = Main_Enet(604,16,151)
    print("create model")
    x = torch.Tensor(local_obs[0])
    # for i in range(5):
    emb_out = main_emb(x)
    print("embedding out:",emb_out)
    # emb = np.array(emb_out.detach().numpy())
    # print("emb:",emb)
    sub_out = sub_emb_out(local_obs)
    print("sub_out:",sub_out)
    e_oth = concat_sub_emb(sub_out)
    
    print("e_oth:", e_oth)

    e_obs = concat_main_sub_emb(emb_out, e_oth)
    print("e_obs:",e_obs)
    print("len of e_obs:", len(e_obs))
    '''
    rail_d, target_d, oth_dir_d, dir_d = depart_obs(obs)
    print("rail_d:",rail_d)
    for row in range(len(rail_d[0])):
        for col in range(len(rail_d[0][row])):
            rail_d[0][row][col] = torch.Tensor(rail_d[0][row][col])
    rail_tensor = torch.Tensor(rail_d[0])
    print("rail_tensor:",rail_tensor)
    main_emb = Main_Enet(25,8,16)
    print("create model")
    y = main_emb(rail_tensor)
    print("y:",y)
    '''
    '''
    print("rail_d:",rail_d)
    print("target_d:",target_d)
    print("oth_dir_d:",oth_dir_d)
    print("dir_d:",dir_d)
    
    print("actions:", actions)
    print("obs:",obs)
    print("rewards:",rewards)
    '''