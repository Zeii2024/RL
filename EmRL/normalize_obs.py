    
    
class Normal_local_obs():
    '''
    将从env获得的local obs标准化
    返回local_obs = {a:local_obs_a}
    local_obs_a : N + 15
    '''
    def __init__(self,obs,num_of_agents):
        self.obs = obs
        self.num_of_agents = num_of_agents

    def shorten_list(self,l:list):
        # 16位缩减到4位
        length = len(l)
        if(length == 16):
            return [float(l[0:4].count(1)),
                    float(l[4:8].count(1)),
                    float(l[8:12].count(1)),
                    float(l[12:16].count(1))]

    def expand_list(self,l):
        # 2位扩展到4位
        if(len(l)==2):
            l.extend([0.0,0.0])
        return l

    def format_local_obs(self):
        # agent a
        local_obs = {}
        for a in range(self.num_of_agents):
            local_obs_a = []
            for row in range(len(self.obs[a][0])):
                for col in range(len(self.obs[a][0][row])):

                    # if compress rail_obs from 16*5*5 to 4*5*5
                    # l0_rail = self.shorten_list(list(self.obs[a][0][row][col]))
                    # otherwise keep rail_obs 16*5*5
                    l0_rail = list(self.obs[a][0][row][col])

                    l0_target = self.expand_list(list(self.obs[a][1][row][col]))
                    l0_oth_dir = list(self.obs[a][2][row][col])
                    
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
        
            local_obs_a.extend(list(self.obs[a][3]))
            # local_obs_a = np.concatenate((obs_rail,obs_target,obs_oth_dir, obs_dir_new),axis=1) 
            local_obs.update({a:local_obs_a})
        
        return local_obs

    def depart_obs(self,obs):
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
        for a in range(self.num_of_agents):
            obs_rail.update({a:self.obs[a][0]})
            obs_target.update({a:self.obs[a][1]})
            obs_oth_dir.update({a:self.obs[a][2]})
            obs_dir.update({a:self.obs[a][3]})

        return obs_rail, obs_target, obs_oth_dir, obs_dir