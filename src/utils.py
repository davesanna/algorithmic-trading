from dataclasses import dataclass
from enum import Enum

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
