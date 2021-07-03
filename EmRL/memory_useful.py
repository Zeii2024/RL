import random
import pickle
import numpy as np
from collections import deque

class Useful_Memory():
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

    def get_useful_memory(self):
        useful_memory_batch = random.sample(self.memory, self.batch_size)
        obs, actions, rewards, new_obs, done = [],[],[],[],[]
        for i in range(len(useful_memory_batch)):
            obs.append(useful_memory_batch[i][0])
            actions.append(useful_memory_batch[i][1])
            rewards.append(useful_memory_batch[i][2])
            new_obs.append(useful_memory_batch[i][3])
            done.append(useful_memory_batch[i][4])

        return obs, actions, rewards, new_obs, done

    def save(self, save_path):
        with open(save_path+"useful_memeory_file.pkl",'wb') as f:
            pickle.dump(self.memory, f)
        print("useful_memory file saved!")

    def load(self, load_path):
        with open(load_path + "useful_memeory_file.pkl", 'rb') as f:
            self.memory = pickle.load(f)