from RLNet import RL_net, Agent
from Embed import Main_Enet, Sub_Enet
from ENV import ENV
from flatland.envs.agent_utils import EnvAgent
from flatland.envs.rail_env import RailEnv, RailEnvActions
# from RLNet import Main_Enet, Sub_Enet
from torch.autograd import Variable
import torch
from Embed import Embed
from memory import Memory
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
                'number_of_agents':1}
speed_ration_map = {1.: 0.,       # Fast passenger train
                    1. / 2.: 1.,  # Fast freight train
                    1. / 3.: 0.,  # Slow commuter train
                    1. / 4.: 0}  # Slow freight train


# input_dim = env_params['number_of_agents'] + 4  #  输入为[x,y,d,s,Mi*N]
# out_dim = len(action_set)         # 输出每个action的Q值

# initiate environment and agents
RE = ENV(env_params=env_params,speed_ration_map=speed_ration_map,obs_builder="local")
env = RE.env()

env_renderer = RE.env_renderer(env)
obs,info = env.reset()
env_renderer.reset()
agents = env.agents

agent = Agent(NO=1,num_of_agents=1,emb_dim=16,hiden_dim=10)   # emb_dim = 16 + N - 1 = N + 15
memory = Memory(1000, 16)

if __name__ == "__main__":
    emb_net = Embed(env_params["number_of_agents"],0)
    obs_emb = emb_net.local_obs_to_emb(obs)
    print("agents.position: ",agents[0].position)
    print("obs_emb:",obs_emb)
    obs_emb = torch.Tensor(obs_emb)
    action = agent.act(obs_emb)
    actions = {0:action}   # only one agent
    print("action:", actions)
    obs_next,rewards, done, _ = env.step(actions)
    obs_next_emb = emb_net.local_obs_to_emb(obs_next)
    print("obs_next_emb:",obs_next_emb)
    obs_next_emb = torch.Tensor(obs_next_emb)
    memory.store_memory(obs_emb,actions,rewards,obs_next_emb,done)
    print("memory:",memory)

    # agent.step(obs_emb,actions,rewards,obs_next_emb,done)

    # action测试成功了
    # TODO 测试agent.step()
