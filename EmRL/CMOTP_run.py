from cmotp import CMOTP
from CMOTP_Agent import Agent
# import time
import torch
# import random
import pickle
# import numpy as np 
from memory import Memory
from memory_useful import Useful_Memory
# from PSD_trainer import Trainer

env = CMOTP()
num_of_agents = 2
input_dim = 6  
action_dim = 5        # [0,1,2,3,4]
MEMORY_SIZE = 1000
BATCH_SIZE = 16
u_memory_size = 100
u_memory_batch = 2
episodes = 200
memory = Memory(MEMORY_SIZE, BATCH_SIZE)
u_memory = Useful_Memory(u_memory_size,u_memory_batch)
# 将其他agent的观测数据乘以obs_rate，以减小它的影响

obs_rate = 0.1

agent = []
for a in range(num_of_agents):
    agent_i = Agent(NO=a,num_of_agents=2,emb_dim=3,hiden_dim=5,action_dim=5)
    agent.append(agent_i)


def load(load_path):
    for a in range(num_of_agents):
        agent[a].load_model(load_path)


def train():
    finish_steps = []
    #time.sleep(2)
    for i_episode in range(episodes):
        # print("______________episode: ", i_episode)
        
        agent1_pos, agent2_pos = env.reset()
        oth_agent2_pos = (*(x*0.1 for x in agent2_pos[:2]), agent2_pos[-1])
        oth_agent1_pos = (*(x*0.1 for x in agent1_pos[:2]), agent1_pos[-1])
        '''
        obs1 = torch.Tensor((*agent1_pos, *oth_agent2_pos))
        obs2 = torch.Tensor((*agent2_pos, *oth_agent1_pos))
        '''
        obs1 = torch.Tensor([*agent1_pos])
        obs2 = torch.Tensor([*agent2_pos])
        obs = {0:obs1, 1:obs2}
        # print("obs: ", obs)

        
        actions = ()
        for a in range(num_of_agents):
            
            action = agent[a].act(obs[a])
            actions = actions + (action,)
        ######
        # print("actions: ", actions)
        env.step(actions)
        

        
        #while mem_len < MEMORY_SIZE:
        steps = 0
        while True:
            steps += 1
            actions = ()
            for a in range(num_of_agents):
                action = agent[a].act(obs[a])
                actions = actions + (action,)
            
            new_agent1_pos, new_agent2_pos, rewards, done, _ = env.step(actions)
            env.render()
            # print("pos1:", new_agent1_pos)
            # print("pos2:", new_agent2_pos)
            new_oth_agent1_pos = (*(x*0.1 for x in new_agent1_pos[:2]), new_agent1_pos[-1])
            new_oth_agent2_pos = (*(x*0.1 for x in new_agent2_pos[:2]), new_agent2_pos[-1])
            '''
            obs1: (5, 4, 1, 0.4, 0.6, 1)
            obs2:(4, 6, 1, 0.5, 0.4, 1)    
            '''
            '''
            new_obs1 = torch.Tensor((*new_agent1_pos, *new_oth_agent2_pos))
            new_obs2 = torch.Tensor((*new_agent2_pos, *new_oth_agent1_pos))
            '''
            '''
            obs1: (5,4,1)
            obs2:(4,6,1)
            '''
            new_obs1 = torch.Tensor([*new_agent1_pos])
            new_obs2 = torch.Tensor([*new_agent2_pos])
            new_obs = {0:new_obs1, 1:new_obs2}

            # store useful memory
            if rewards[0] == 5 or rewards[0] == 10:
                u_memory.store_memory(obs,actions,rewards,new_obs,done)
                if rewards[0]==5:
                    print("hold goods")
                else:
                    print("finish target")
            
            memory.store_memory(obs,actions,rewards,new_obs,done)
            mem_len = memory.memory_counter

            if mem_len >= MEMORY_SIZE:
                batch_rewards = {}
                obs_batch,action_batch,reward_batch,obs_next_batch,done_batch=memory.get_replay_batch()
                for i in range(num_of_agents):
                    reward = agent[i].step(obs_batch,action_batch,reward_batch,obs_next_batch,done_batch)
                    batch_rewards.update({i:reward})
                
                print("\r","episode:{a}, steps:{b}".format(a=i_episode,b=steps),end=' ',flush=True)

            if done[0] or done[1]:
                finish_steps.append(steps)
                for a in range(num_of_agents):
                    agent[a].save_model('D:/桌面/My_TTP/EmRL/save/')
                break
                
            if steps > 2000:
                finish_steps.append(steps)
                steps = 0
                print("--")
                break
            
            # use useful_memory
            if steps % 500 == 0 and u_memory.memory_counter > u_memory_batch:
                u_obs,u_actions,u_rewards,u_new_obs,u_done = u_memory.get_useful_memory()
                for i in range(len(u_obs)):
                    memory.store_memory(u_obs[i],u_actions[i],u_rewards[i],u_new_obs[i],u_done[i])
                # print("+")
                print("--use %d u_memory" % u_memory_batch)

            obs = new_obs
    with open('D:/桌面/My_TTP/EmRL/save/finish_steps.pkl','wb') as f:
        pickle.dump(finish_steps,f)

if __name__ == '__main__':
    load_path = 'D:/桌面/My_TTP/EmRL/save/'
    # load(load_path)
    train()
    for a in range(num_of_agents):
        agent[a].show()
