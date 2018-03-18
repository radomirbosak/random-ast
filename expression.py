import random

from variable import generate_variable
from literal import generate_literal


def generate_expression():
    choices = [
        generate_variable,
        generate_literal,
    ]
    return random.choice(choices)()
