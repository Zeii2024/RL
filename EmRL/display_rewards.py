import matplotlib.pyplot as plt 
import pickle

def read_file():
    file_path = "D:/桌面/rewards_list_2000.pkl"
    with open(file_path,'rb') as f:
        rewards = pickle.load(f)
    print(rewards)
    print(len(rewards))
    return rewards

def show(rewards):
    num_of_agents = len(rewards[0]) - 1 
    x = range(len(rewards))
    rewards_list = []
    for a in range(num_of_agents):
        l = []
        for i in x:
            l.append(rewards[i][a])
        rewards_list.append(l)

    
    plt.plot(x,rewards_list[0],'-')
    #plt.plot(x,rewards_list[0],'o')
    plt.xlabel("episodes")
    plt.ylabel("rewards") 



    plt.show()

show(read_file())
#rl = read_file()
