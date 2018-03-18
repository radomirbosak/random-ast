import random

from variable import generate_variable
from literal import generate_literal


def generate_expression(max_depth=None):
    choices = [
        generate_variable,
        generate_literal,
    ]
    return random.choice(choices)(max_depth=max_depth)
