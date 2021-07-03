from cmotp import CMOTP
from CMOTP_Agent import Agent
import time
import torch
import random
import pickle
import numpy as np 
from memory import Memory
from PSD_trainer import Trainer

env = CMOTP()
num_of_agents = 2
input_dim = 6  
action_dim = 5        # [0,1,2,3,4]
MEMORY_SIZE = 1000
BATCH_SIZE = 32
episodes = 1000
memory = Memory(MEMORY_SIZE, BATCH_SIZE)

agent = []
load_path = 'D:/桌面/My_TTP/EmRL/save/'
for a in range(num_of_agents):
    agent_i = Agent(NO=a,num_of_agents=2,emb_dim=6,hiden_dim=5,action_dim=5)
    agent_i.load_model(load_path)
    agent.append(agent_i)

def test():
    for i_episode in range(episodes):
        print("______________episode: ", i_episode)
        
        agent1_pos, agent2_pos = env.reset()
        obs1 = torch.Tensor((*agent1_pos, *agent2_pos))
        obs2 = torch.Tensor((*agent2_pos, *agent1_pos))
        obs = {0:obs1, 1:obs2}
        # print("obs: ", obs)

        
        actions = ()
        for a in range(num_of_agents):
            action = agent[a].act(obs[a])
            actions = actions + (action,)
        ######
        print("actions: ", actions[1])
        env.step(actions)
        env.render()

        #while mem_len < MEMORY_SIZE:
        steps = 0
        while True:
            steps += 1
            actions = ()
            for a in range(num_of_agents):
                action = agent[a].act(obs[a])
                actions = actions + (action,)
            
            new_agent1_pos, new_agent2_pos, rewards, done, _ = env.step(actions)
            # print("pos1:", new_agent1_pos)
            # print("pos2:", new_agent2_pos)
            
            new_obs1 = torch.Tensor((*new_agent1_pos, *new_agent2_pos))
            new_obs2 = torch.Tensor((*new_agent2_pos, *new_agent1_pos))
            new_obs = {0:new_obs1, 1:new_obs2}

            env.render()
            time.sleep(0.1)

            if done[0] or done[1]:
                print("episode: {a} done with {b} steps".format(i_episode,steps))
                break
                
            if steps > 5000:
                print("NOT done within 5000 steps!")
                steps = 0
                break

            obs = new_obs


if __name__ == '__main__':
    test()
    for a in range(num_of_agents):
        agent[a].show()