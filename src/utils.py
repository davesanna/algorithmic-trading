from enum import Enum
# The properties of an enumeration are useful for defining an immutable, 
# related set of constant values that may or may not have a semantic meaning.



class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Colors(Enum):
    WHITE = (255, 255, 255)
    RED = (200,0,0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    BLACK = (0,0,0)