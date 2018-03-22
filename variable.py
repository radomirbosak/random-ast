import ast
import random

from words import generate_variable_name


def generate_variable(max_depth=None, ctx=ast.Load()):
    name = generate_variable_name()
    return ast.Name(name, ctx)


def generate_variable_tuple(max_depth=None, ctx=ast.Load()):
    num_elts = random.randrange(2, 4)
    elts = [generate_variable(max_depth=max_depth, ctx=ctx) for _ in range(num_elts)]
    return ast.Tuple(elts, ctx)


def generate_variable_or_tuple(max_depth=None, ctx=ast.Load()):
    choices = [generate_variable, generate_variable_tuple]
    return random.choice(choices)(max_depth=max_depth, ctx=ctx)
