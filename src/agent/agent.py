from typing import final
import torch
import random
import numpy as np
from game.snake import SnakeGameAI
from utils import Direction, Point
from model.model import LinearQNet, QTrainer

from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0  # control randomness
        self.gamma = 0.9  # discount rate, 0<x<1
        self.memory = deque(
            maxlen=MAX_MEMORY
        )  # removes automatically from left side (popleft) when maxmemory is exceded
        self.model = LinearQNet(11, 256, 3)  # TODO
        self.trainer = QTrainer(
            model=self.model, learning_rate=LR, gamma=self.gamma
        )  # TODO

    def get_state(self, game):
        head = game.head
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_u = game.direction == Direction.UP
        dir_r = game.direction == Direction.RIGHT
        dir_d = game.direction == Direction.DOWN
        dir_l = game.direction == Direction.LEFT

        state = [
            # danger straight
            (dir_r and game.is_collision(point_r))
            or (dir_u and game.is_collision(point_u))
            or (dir_l and game.is_collision(point_l))
            or (dir_d and game.is_collision(point_d)),
            # danger right
            (dir_r and game.is_collision(point_d))
            or (dir_u and game.is_collision(point_r))
            or (dir_l and game.is_collision(point_u))
            or (dir_d and game.is_collision(point_l)),
            # danger left
            (dir_r and game.is_collision(point_u))
            or (dir_u and game.is_collision(point_l))
            or (dir_l and game.is_collision(point_d))
            or (dir_d and game.is_collision(point_r)),
            # current directions bool
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # food position
            game.food.x < head.x,  # food left
            game.food.x > head.x,  # food right
            game.food.y < head.y,  # food up
            game.food.y > head.y,  # food down
        ]

        return np.array(state, dtype=int)

    def get_action(self, state):
        # random moves: exploration vs exploitation
        self.epsilon = (
            80 - self.n_games
        )  # > n_games => < epsilon => < random moves => < exploration & > exploitation
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            prediction = self.model(
                torch.tensor(state, dtype=torch.float)
            )  # pytorch does not have .predict; calling the model with the input, directly executes the implemented forward method
            move = torch.argmax(prediction).item()

        final_move[move] = 1

        return final_move

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append(
            (state, action, reward, next_state, game_over)
        )  # is deque, popleft if > maxmemory

    def train_long_memory(self):

        sample = (
            random.sample(self.memory, BATCH_SIZE)
            if len(self.memory) > BATCH_SIZE
            else self.memory
        )

        states, actions, rewards, next_states, game_overs = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
