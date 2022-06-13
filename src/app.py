#!/usr/bin/env python

import pygame
from pygame.locals import *
from game.snake import SnakeGame


def main():
    pygame.init()
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over:
            break
    print(f"Final Score: {score}")
    pygame.quit()


if __name__ == "__main__":
    main()
