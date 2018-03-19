import ast
import random

from variable import generate_variable
from literal import generate_literal


def generate_expression(max_depth=None):
    choices = [
        generate_variable,
        generate_literal,
    ]
    if max_depth >= 1:
        choices += [generate_unary_op]

    return random.choice(choices)(max_depth=max_depth)


def generate_unary_op(max_depth=None):
    choices = [
        ast.UAdd,
        ast.USub,
        ast.Not,
        ast.Invert,
    ]
    value = generate_expression(max_depth=max_depth - 1)
    op = random.choice(choices)
    return ast.UnaryOp(op(), value)
