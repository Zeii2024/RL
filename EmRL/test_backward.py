import Agent_for_gym
import torch
import torch.nn as nn

'''
Test how backward works
'''


class RL_net(torch.nn.Module):
    '''
    input: embedding of obs
    output: values of actions
    '''
    def __init__(self,in_feature,out_feature,hiden_feature=16):  # hiden_dim = 16
        super(RL_net,self).__init__()
        self.fc1 = nn.Linear(in_feature, hiden_feature)
        # self.fc1.weight.data.normal_(0,0.1)  # initialize
        self.tanh = nn.Tanh()
        self.fc2 = nn.Linear(hiden_feature,out_feature)
        # self.fc2.weight.data.normal_(0,0.1)  # initialize

    def forward(self,x):
        x = self.fc1(x)
        x = self.tanh(x)
        x = self.fc2(x)

        return x


class Train():
    def __init__(self):
        self.net = RL_net(4,5,3)
        self.t_net = RL_net(4,5,3)
        self.epochs = 100
        self.x = torch.tensor([0.1,0.2,0.3,0.4])

        self.y = torch.tensor([0.1, 0.2, 0.1, 1, 4.]) # label
        # loss_f
        self.loss_f = nn.MSELoss(reduction='none')
        # optimizer
        self.opt = torch.optim.Adam(self.net.parameters(),lr=0.01)

    def trainer(self):
        for i in range(self.epochs):
            print("paras:",self.net.state_dict())
            out = self.net(self.x)
            # 让lable与out只有一个值不同，其他值都相同
            lable = out.clone().detach()
            lable[2] = 1.67

            print("out:",out)
            print("lable:",lable)
            loss = self.loss_f(out,lable)
            print("loss:",loss)
            self.opt.zero_grad()
            loss.backward(torch.ones_like(out))
            
            self.opt.step()
        
        # 测试复制更新网络参数
        out_t1 = self.t_net(self.x)
        self.t_net.load_state_dict(self.net.state_dict())
        out_t2 = self.t_net(self.x)
        print("out_t1:", out_t1)
        print("out_t2:", out_t2)


t = Train()
t.trainer()