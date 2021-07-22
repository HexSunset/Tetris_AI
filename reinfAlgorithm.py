from tensorforce.environments import Environment
from tensorforce.agents import Agent
from tensorforce.execution import Runner
import numpy as np


class CustomEnvironment(Environment):

    def __init__(self):
        super().__init__()

    def states(self):
        return dict(type='float', shape=(8,))

    def actions(self):
        return dict(type='int', num_values=4)

    def reset(self):
        state = np.random.random(size=(8,))
        return state

    def execute(self, actions):
        next_state = np.random.random(size=(8,))
        terminal = np.random.random() < 0.5
        reward = np.random.random()
        return next_state, terminal, reward

    #variables with numpy's random function should get data from the game i'm guessing

class nnAlgorithm():
    def __init__(self):
        self.environment = Environment.create(
        environment=CustomEnvironment, max_episode_timesteps=500
        )

        self.agent = Agent.create(
        agent='tensorforce', environment=self.environment, update=64,
        optimizer=dict(optimizer='adam', learning_rate=1e-3),
        objective='policy_gradient', reward_estimation=dict(horizon=20)
        )

    def train(n):
        for _ in range(n):
            states = environment.reset()
            terminal = False
            while not terminal:
                actions = agent.act(states=states)
                states, terminal, reward = environment.execute(actions=actions)
                agent.observe(terminal=terminal, reward=reward