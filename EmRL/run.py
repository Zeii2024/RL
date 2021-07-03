
from RLNet import Agent
import time
import torch
import random
import pickle
import numpy as np 
from ENV import ENV
from memory import Memory
from train import Trainer
from flatland.envs.agent_utils import EnvAgent
from flatland.envs.rail_env import RailEnv, RailEnvActions

action_set = ['DO_NOTHING','MOVE_LEFT','MOVE_FORWARD','MOVE_RIGHT','STOP_MOVING']
'''
directions = {"North" : 0,
              "East"  : 1,
              "South" : 2,
              "West"  : 3}

agent.handle = int 0
agent_positions[position] = -1 ---> cell可用，未被占用
agent_positions[position] = agent.handle -----> cell被占用
'''

# environment
env_params = {'width': 40,
                'height': 40,
                'max_num_cities': 6,
                'number_of_agents':4}
speed_ration_map = {1.: 1.,       # Fast passenger train
                    1. / 2.:0.,  # Fast freight train
                    1. / 3.: 0.,  # Slow commuter train
                    1. / 4.: 0.}  # Slow freight train

# memory param

# initiate environment and agents
RE = ENV(env_params=env_params,speed_ration_map=speed_ration_map,obs_builder="local")
env = RE.env()
env_renderer = RE.env_renderer(env)
obs,info = env.reset()
env_renderer.reset()
agents = env.agents
num_of_agents = env.get_num_agents()
input_dim = num_of_agents + 15  # env_params['number_of_agents'] + 4  #  输入为[x,y,d,s,Mi*N]
action_dim = len(action_set)         # 输出每个action的Q值
MEMORY_SIZE = 800
BATCH_SIZE = 32
epochs = 100
memory = Memory(MEMORY_SIZE, BATCH_SIZE)
# save agents initial information for resteting agents
agent = []
agents_init_info = []
last_position = {} # 记录agent上个位置
for a in range(env.get_num_agents()):
    temp =  Agent(a, num_of_agents,input_dim,hiden_dim=10,action_dim=action_dim)
    agent.append(temp)
    agents_init = {"initial_position":agents[a].initial_position,
                    "position":agents[a].position,
                    "direction":agents[a].direction,
                    "target":agents[a].target,
                    "speed_data":agents[a].speed_data,
                    "moving":agents[a].moving,
                    "status":agents[a].status,
                    "old_position":agents[a].old_position,
                    "old_direction":agents[a].old_direction,
                    "handle":agents[a].handle}
    agents_init_info.append(agents_init)
    
    last_position.update({a:agents[a].old_position})

trainer = Trainer(memory,agent,epochs,agents_init_info)


if __name__ == '__main__':
    # TODO 八成是obs的问题
    # TODO 或者reward的问题
    # TODO 会不会不太适合这种从memory中取样训练的方式
    print("agent_target:",agents_init_info[a]['target'])
    print("agent_init_position:",agents_init_info[a]['initial_position'])
    time.sleep(2)
    trainer.train(env,env_renderer)
    
    # agents
    for a in range(num_of_agents):
        agent[a].show(show_acc=False)

