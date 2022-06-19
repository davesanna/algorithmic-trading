#!/usr/bin/env python

import matplotlib.pyplot as plt
from pygame.locals import *
from game.snake import SnakeGameAI
from agent.agent import Agent
from utils import plot


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    plt.ion()

    while True:
        # get previous state
        state_old = agent.get_state(game)

        # predict move based on old state
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # remember
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory (replay memory/experience replay); trains on all previous moves
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            # plot results
            total_score += score
            mean_score = total_score / agent.n_games
            plot_scores.append(score)
            plot_mean_scores.append(mean_score)
            print("Game: ", agent.n_games, "Score: ", score, "Record: ", record)

            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
