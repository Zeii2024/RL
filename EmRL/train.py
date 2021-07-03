# from Embed import Embed
from collections import deque

class Trainer():
    '''
    从memory拿到replay batch
    所有agent同步训练，使用相同的replay batch
    如果done,奖励值从这里给出

    agent: dict of agents_net: {0:agent_0, 1:agent_1}
    memory: memory pool

    '''

    def __init__(self, memory, agent:dict, epochs,agents_init_info):
        self.memory = memory
        self.agent = agent
        self.epochs = epochs
        self.agents_init_info = agents_init_info
        self.num_of_agents = len(agent)
        self.save = True
        

    def train(self,env,env_renderer):
        initial_actions = {}
        for a in range(self.num_of_agents):
            initial_actions.update({a:0})

        obs,_,_,_ = env.step(initial_actions) # no env.reset()
        # print("obs:",obs)
        # 记录每个episode的reward平均值之和，作为最终的评价标准
        rewards_que = deque(maxlen=1000)

        for epoch in range(self.epochs):
            print("episode:",epoch)
            e_rewards = 0
            steps = 0
            while True:
                steps += 1
                len_memory = self.memory.memory_counter
                # 当记忆条数达到batch_size的5倍时，取batch训练
                if(len_memory > self.memory.batch_size * 5):
                    obs_batch,action_batch,reward_batch,obs_next_batch,done = self.memory.get_replay_batch()
                    
                    rewards = {}
                    for a in range(self.num_of_agents):
                        # reward
                        reward = self.agent[a].step(obs_batch,action_batch,reward_batch,obs_next_batch,done)
                        ############################################
                        # if reward<0: reward = 0
                        ############################################
                        if rewards.get(a):
                            reward = rewards[a] + reward
                        rewards.update({a:reward})
                    # print("steps:{a} rewards:{b}".format(a=steps,b=rewards))    


                        
                # env step and store memory  
                actions = {}
                obs_emb = {}
                obs_new_emb = {}
                for a in range(self.num_of_agents):
                    obs_emb_i = self.agent[a].emb(obs)
                    '''
                    actions = [0,1,2,3,4]
                    act_valid = [0,0,0,0,0]
                    for i in actions:
                        cell_free,new_cell_valid,new_direction,new_position,transition_valid = env._check_action_on_agent(i,env.agents[a])
                        if cell_free and new_cell_valid:
                            

                    '''
                    action = self.agent[a].act(obs_emb_i)
                    obs_emb.update({a:obs_emb_i})
                    actions.update({a:action})

                '''  TODO 测试1  '''
                # 测试下obs_emb与position是否具有一致性
                # 当遇到相同的postion时，将position和obs_emb写入文档，
                # 比较相同的position,它们的obs_emb是否相同
                # 每个step所有agent的reward和
                step_reward = 0.0
                obs_new, reward_new, done_new, _ = env.step(actions)
                env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
                for a in range(self.num_of_agents):
                    obs_new_i = self.agent[a].emb(obs_new)
                    obs_new_emb.update({a:obs_new_i})

                    step_reward += reward_new[a]
                    # if done_new[a]:
                        # env.reset_agent(a, self.agents_init_info[a])
                        # env_renderer.reset()
                # 一个step的reward的平均值        
                aver_reward = step_reward / self.num_of_agents
                # 一个episode的平均reward的和
                e_rewards += aver_reward

                self.memory.store_memory(obs_emb,actions,reward_new,obs_new_emb,done_new) # obs_next
                
                if done_new['__all__'] or steps > 499:
                    # 将e_rewards存入队列
                    rewards_que.append(e_rewards)
                    print("episode_average_rewards:",e_rewards)
                    if done_new['__all__']:
                        print("******* all done *******")
                    else:
                        print("------- out steps -------")
                    for a in range(self.num_of_agents):
                        env.reset_agent(a,self.agents_init_info[a])
                    break

                obs = obs_new


        if self.save:
            save_path = 'D:/桌面/My_TTP/EmRL/save/'
            for a in range(self.num_of_agents):
                self.agent[a].save_model(save_path)
            with open(save_path+'rewards_que.pkl','wb') as f:
                f.dump(rewards_que)
            
            env.save(save_path+'env.pkl')
            print("Env saved!")
            