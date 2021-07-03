
import random
import pickle
import numpy as np
from collections import deque

class Memory():
    '''
    所有agent同步训练，它们拿到的replay应该是一样的
    '''

    def __init__(self, memory_size,batch_size):
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.memory = self.create_memory_pool()
        self.memory_counter = 0

    def create_memory_pool(self):
        memory = deque(maxlen=self.memory_size)
        
        return memory

    def store_memory(self,obs, actions, rewards,obs_next, done):
        self.memory.append([obs,actions,rewards,obs_next,done])
        if self.memory_counter < self.memory_size:
            self.memory_counter += 1

    def get_replay_batch(self):
        if self.memory_counter < self.batch_size:
            print("memory records are not enough!")
            return None
        obs_batch,action_batch,reward_batch,obs_next_batch,done_batch = [],[],[],[],[]    
        replay_batch = random.sample(self.memory, self.batch_size)
        
        # 先直接返回batch
        # return replay_batch

        for replay in replay_batch:
            obs_batch.append(replay[0])
            action_batch.append(replay[1])
            reward_batch.append(replay[2])
            obs_next_batch.append(replay[3])
            done_batch.append(replay[4])

        return obs_batch,action_batch,reward_batch,obs_next_batch,done_batch

    def save(self, save_path):
        with open(save_path+"memeory_file.pkl",'wb') as f:
            pickle.dump(self.memory, f)
        print("memory file saved!")

    def load(self, load_path):
        with open(load_path, 'rb') as f:
            self.memory = pickle.load(f)

