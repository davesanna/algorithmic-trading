from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
from IPython import display

# The properties of an enumeration are useful for defining an immutable,
# related set of constant values that may or may not have a semantic meaning.


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


@dataclass
class Colors:
    WHITE: tuple = (255, 255, 255)
    RED: tuple = (200, 0, 0)
    BLUE1: tuple = (0, 0, 255)
    BLUE2: tuple = (0, 100, 255)
    BLACK: tuple = (0, 0, 0)


@dataclass
class Point:
    x: int
    y: int


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training ...")
    plt.xlabel("Number of Games")
    plt.ylabel("Score")

    plt.plot(scores)
    plt.plot(mean_scores)

    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))

    plt.show(block=False)
    plt.pause(
        0.1
    )  # https://www.geeksforgeeks.org/matplotlib-pyplot-pause-in-python/#:~:text=The%20pause()%20function%20in,to%20pause%20for%20interval%20seconds.&text=Parameters%3A%20This%20method%20does%20not,does%20not%20returns%20any%20value.
