import time

import numpy as np

# TERE IS NO MalfunctionParameters in malfunction_generators !
from flatland.envs.malfunction_generators import malfunction_from_params  # MalfunctionParameters
from flatland.envs.observations import TreeObsForRailEnv, GlobalObsForRailEnv, LocalObsForRailEnv
from flatland.envs.predictions import ShortestPathPredictorForRailEnv
from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.schedule_generators import sparse_schedule_generator
from flatland.utils.rendertools import RenderTool, AgentRenderVariant

np.random.seed(1)

# Use the new sparse_rail_generator to generate feasible network configurations with corresponding tasks
# Training on simple small tasks is the best way to get familiar with the environment
env_params = {'width': 30,
                'height': 30,
                'max_num_cities': 5,
                'number_of_agents': 1}
speed_ration_map = {1.: 0.,       # Fast passenger train
                    1. / 2.: 0.,  # Fast freight train
                    1. / 3.: 0.,  # Slow commuter train
                    1. / 4.: 1.}  # Slow freight train

class ENV():

    def __init__(self,env_params=env_params, speed_ration_map=speed_ration_map,obs_builder="global"):
        '''
        obs_builder: GlobalObsForRailEnv, LocalObsForRainEnv, TreeObsForRailEnv
        '''
        self.width = env_params['width']
        self.height = env_params['height']
        self.max_num_cities = env_params['max_num_cities']
        self.number_of_agents = env_params['number_of_agents']
        # Use a the malfunction generator to break agents from time to time
        self.stochastic_data = {'malfunction_rate':0,  # Rate of malfunction occurence
                            'min_duration':0,  # Minimal duration of malfunction
                            'max_duration':0  # Max duration of malfunction
                                                }
        # Custom observation builder
        self.TreeObservation = TreeObsForRailEnv(max_depth=2, predictor=ShortestPathPredictorForRailEnv())
        
        # Different agent types (trains) with different speeds.
        self.speed_ration_map = speed_ration_map 
        # obs builder list
        self.obs_builder_dict = {"global": GlobalObsForRailEnv,
                                "local": LocalObsForRailEnv(view_width=2,view_height=5,center=3),
                                "tree": TreeObsForRailEnv(max_depth=2, predictor=ShortestPathPredictorForRailEnv())}
        self.obs_builder = obs_builder

    def env(self):
        # obs builder
        obs_builder_object = self.obs_builder_dict[self.obs_builder]

        env = RailEnv(width=self.width,  # width和height是网格grid的数量
                    height=self.height,
                    rail_generator=sparse_rail_generator(max_num_cities=self.max_num_cities,
                                                        # Number of cities in map (where train stations are)
                                                        seed=19,  # Random seed
                                                        grid_mode=True,
                                                        max_rails_between_cities=2,
                                                        max_rails_in_city=2,
                                                        ),
                    schedule_generator=sparse_schedule_generator(self.speed_ration_map),
                    number_of_agents=self.number_of_agents,
                    malfunction_generator_and_process_data=malfunction_from_params(self.stochastic_data),
                    # Malfunction data generator
                    obs_builder_object=obs_builder_object,
                    remove_agents_at_target=False,
                    record_steps=True
                    )
        return env
    
    def env_renderer(self, env):
        # RailEnv.DEPOT_POSITION = lambda agent, agent_handle : (agent_handle % env.height,0)
        # To show the screen
        
        env_renderer = RenderTool(env, gl="PILSVG",
                                agent_render_variant=AgentRenderVariant.AGENT_SHOWS_OPTIONS_AND_BOX,
                                show_debug=True,
                                screen_height=800,
                                screen_width=800)
        return env_renderer

# Import your own Agent or use RLlib to train agents on Flatland
# As an example we use a random agent instead
class RandomAgent:

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

    def act(self, state):
        """
        根据observation做出action，因此对observation每条数据要弄清楚
        用上其中有用的
        :param state: input is the observation of the agent
        :return: returns an action
        """
        return 2  # np.random.choice(np.arange(self.action_size))

    def step(self, memories):
        """
        Step function to improve agent by adjusting policy given the observations

        :param memories: SARS Tuple to be
        :return:
        """
        return

    def save(self, filename):
        # Store the current policy
        return

    def load(self, filename):
        # Load a policy
        return


if __name__ == '__main__':
    # Initialize the agent with the parameters corresponding to the environment and observation_builder
    # Set action space to 4 to remove stop action
    agent = RandomAgent(12, 4)
    RE = ENV()
    env = RE.env()
    env_renderer = RE.env_renderer(env)
    # Empty dictionary for all agent action
    action_dict = dict()

    print("Start episode...")
    # Reset environment and get initial observations for all agents
    start_reset = time.time()
    obs, info = env.reset()
    print("obs:",obs)
    # print("obs_shape:",obs.shape())
    # print("obs: ",obs[0][0],"\n",obs[0][1],"\n",obs[0][2])
    end_reset = time.time()
    print("reset time: ",end_reset - start_reset)
    print("num of agents: ",env.get_num_agents(), )
    # Reset the rendering sytem
    env_renderer.reset()

    # Here you can also further enhance the provided observation by means of normalization
    # See training navigation example in the baseline repository
'''
    score = 0
    # Run episode
    frame_step = 0
    debug = True
    for step in range(5000):
        # Chose an action for each agent in the environment
        for a in range(env.get_num_agents()):
            action = agent.act(obs[a])
            action_dict.update({a: action})

        # Environment step which returns the observations for all agents, their corresponding
        # reward and whether their are done
        # next_obs[0][1][0] = [-1,-1,-1,-1,0] * width
        # obs[0] 的个数 = agents的个数
        # obs[0][1] 的个数 = height
        # obs[0][1][0] 的个数 = width
        # obs[0][1][0][0] 的个数 = 5
        # env中的width和height是grid的个数，每一个格子用一个五维数组来表示

        next_obs, all_rewards, done, _ = env.step(action_dict)
        if step is 61:
            for h in range(RE.height):
                for w in range(RE.width):
                    pass
                    # print("action_dict: ", action_dict)
                    #print("next_obs[0][1][{}][{}]:".format(h,w),next_obs[0][1][h][w])
            debug = False
        env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
        # if step is 61:
            # time.sleep(1)
        frame_step += 1
        # Update replay buffer and train agent
        for a in range(env.get_num_agents()):
            agent.step((obs[a], action_dict[a], all_rewards[a], next_obs[a], done[a]))
            score += all_rewards[a]

        obs = next_obs.copy()
        if done['__all__']:
            break

    print('Episode: Steps {}\t Score = {}'.format(step, score))
    #  env.save_episode("saved_episode_2.mpk")
'''