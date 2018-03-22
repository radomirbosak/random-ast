import ast
import random

from expression import generate_expression
from variable import generate_variable_or_tuple


def generate_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    targets = [generate_variable_or_tuple(max_depth=max_depth, ctx=ast.Store())]
    return ast.Assign(targets, value)


def generate_statement(max_depth=None):
    choices = [
        generate_assign,
    ]
    return random.choice(choices)(max_depth=max_depth)
