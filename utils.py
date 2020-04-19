import math

def is_square(integer):
    root = math.sqrt(integer)
    return integer == int(root + 0.5) ** 2