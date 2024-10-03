import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import gym
from gym.wrappers import StepAPICompatibility

# 创建 Gym 环境并启用新 step API
env = gym.make('CartPole-v1')
env = StepAPICompatibility(env, new_step_api=True)

# 获取状态和动作空间的大小
state_size = env.observation_space.shape[0]
action_size = env.action_space.n

# 定义一个通用的DQN网络
class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# 定义强化学习参数
gamma = 0.99
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
learning_rate = 0.001
batch_size = 64
memory_size = 2000

# 初始化Q网络、目标网络和优化器
q_network = DQN(state_size, action_size)
target_network = DQN(state_size, action_size)
optimizer = optim.Adam(q_network.parameters(), lr=learning_rate)
memory = deque(maxlen=memory_size)

def choose_action(state):
    if np.random.rand() <= epsilon:
        return random.randrange(action_size)
    else:
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = q_network(state)
        return torch.argmax(q_values).item()

def replay():
    if len(memory) < batch_size:
        return
    batch = random.sample(memory, batch_size)
    for state, action, reward, next_state, done in batch:
        target = reward
        if not done:
            next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
            target += gamma * torch.max(target_network(next_state)).item()
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = q_network(state)
        q_target = q_values.clone()
        q_target[0][action] = target
        loss = nn.functional.mse_loss(q_values, q_target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# 训练DQN智能体
episodes = 1000
for e in range(episodes):
    state = env.reset()  # 重置环境
    done = False
    while not done:
        action = choose_action(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        memory.append((state, action, reward, next_state, done))
        state = next_state
        replay()

    if epsilon > epsilon_min:
        epsilon *= epsilon_decay

    # 更新目标网络
    if e % 10 == 0:
        target_network.load_state_dict(q_network.state_dict())

print("训练完成!")
