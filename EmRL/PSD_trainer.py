import time
import torch
import pickle

class Trainer():
    '''
    从memory拿到replay batch
    所有agent同步训练，使用相同的replay batch
    如果done,奖励值从这里给出

    agent: dict of agents_net: {0:agent_0, 1:agent_1}
    memory: memory pool

    '''

    def __init__(self, memory, agent:dict, episodes,agents_init_info):
        self.memory = memory
        self.agent = agent
        self.episodes = episodes
        self.agents_init_info = agents_init_info
        self.num_of_agents = len(agent)
        self.save = True
        self.train_rewards = {}
        for i in range(self.num_of_agents):
            self.train_rewards.update({i:[]})

    def collect_obs(self, agents):
        '''
        obs: dict -- 4 elements
            |--position: x, y ---- float
            |--direction: d ---- float
            |--speed: s ---- float
        '''
        # get obs dict
        # agents = env.agents
        obs = {} 
        
        for a in range(self.num_of_agents):
            obs_a = []
            obs_a.append(float(agents[a].position[0]))
            obs_a.append(float(agents[a].position[1]))
            obs_a.append(float(agents[a].direction))
            obs_a.append(float(agents[a].speed_data['speed']))

            obs_a = torch.Tensor(obs_a)

            obs.update({a : obs_a})
            
        
        # print("obs: ", obs)
        # env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
        # time.sleep(10)
        return obs


    def train(self,env,env_renderer):
        
        '''
        一次done是一个episode

        initial_actions = {}
        for a in range(self.num_of_agents):
            initial_actions.update({a:0})

        obs,_,_,_ = env.step(initial_actions) # no env.reset()
        '''
        '''
        
        '''
        # rewards_list = []
        for episode in range(self.episodes):

            agents = env.agents
            obs = self.collect_obs(agents)
            steps = 0
            if episode > 0:
                for i in range(self.num_of_agents):
                    self.train_rewards[i].append(episode_reward[i])
            episode_reward = {}
            for i in range(self.num_of_agents):
                episode_reward.update({i:0})
            
            while True:
                steps += 1
                len_memory = self.memory.memory_counter
                # 当记忆条数达到batch_size的10倍时，取batch训练
                if(len_memory > self.memory.batch_size * 10):
                    obs_batch,action_batch,reward_batch,obs_next_batch,done = self.memory.get_replay_batch()
                    #replay_batch = self.memory.get_replay_batch()
                    
                    rewards = {}
                    for a in range(self.num_of_agents):
                        # reward
                        reward = self.agent[a].step(obs_batch,action_batch,reward_batch,obs_next_batch,done)
                        # reward = self.agent[a].step(replay_batch)
                        ############################################
                        # if reward<0: reward = 0
                        ############################################
                    
                        if rewards.get(a):
                            reward = rewards[a] + reward
                        rewards.update({a:reward})
                    # print("rewards:",rewards)    
                    # print('\r',"episode:{a}, steps:{b},rewards:{c}".format(a=episode,b=steps,c=rewards))

                actions = {}
               
                # obs_new_emb = {}
                for a in range(self.num_of_agents):
                    agent_actions = [0,1,2,3,4]
                    # 初始化都为0,把可行的动作标记为1
                    actions_valid = [0,0,0,0,0]
                    # 先找到可行的动作
                    for i in agent_actions:
                        cell_free,new_cell_valid,new_direction,new_position,transition_valid = env._check_action_on_agent(i,env.agents[a])
                        if cell_free and new_cell_valid and transition_valid:
                            actions_valid[i] = 1
                    # print("position:",agents[a].position)
                    # print("actions_valid:", actions_valid)
                    
                    # action=0时，agent可以走也可以不走，这是个违法的动作，禁用它
                    actions_valid[0] = 0

                    action = self.agent[a].act(obs[a], actions_valid)
                    actions.update({a:action})

                # env step
                _, reward_new, done_new, _ = env.step(actions)
                agents = env.agents
                obs_new = self.collect_obs(agents)
                # print("obs_new: ", obs_new)
                for i in range(self.num_of_agents):
                    episode_reward[i] += reward_new[i]
            
                env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
                # print("memory:",obs,actions,reward_new,obs_new,done_new)
                self.memory.store_memory(obs,actions,reward_new,obs_new,done_new) # obs_next
                obs = obs_new

                if done_new['__all__']:
                    print("done")
                    print("episode reward:", episode_reward)
                    # rewards_list.append(episode_reward)
                    for a in range(self.num_of_agents):
                        env.reset_agent(a, self.agents_init_info[a])
                    break
                
                if steps > 119:
                    print("steps out")
                    print("episode reward:", episode_reward)
                    # rewards_list.append(episode_reward)
                    for a in range(self.num_of_agents):
                        env.reset_agent(a, self.agents_init_info[a])
                    break

                

        if self.save:
            save_path = 'D:/桌面/My_TTP/EmRL/save/'
            for a in range(self.num_of_agents):
                self.agent[a].save_model(save_path)
            env.save(save_path+'env.pkl')
            print("Env saved!")

            # save train rewards
            with open(save_path+'train_rewards.pkl','wb') as f:
                pickle.dump(self.train_rewards, f)


