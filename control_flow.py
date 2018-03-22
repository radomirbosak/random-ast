import ast
import random

from variable import generate_variable_or_tuple
from expression import generate_expression
from statement import generate_statement


MAX_STATEMENTS = 5


def generate_block(max_depth=None):
    num_statements = random.randrange(1, MAX_STATEMENTS)
    choices = [
        generate_statement,
    ]
    if max_depth >= 1:
        choices += [
            generate_if,
            generate_for,
        ]

    nodes = random.choices(choices, k=num_statements)

    return [node(max_depth=max_depth - 1) for node in nodes]


def generate_if(max_depth=None):
    test = generate_expression(max_depth=max_depth)
    body = generate_block(max_depth=max_depth)
    orelse = random.choice([generate_block(max_depth=max_depth), []])
    return ast.If(test, body, orelse)


def generate_for(max_depth=None):
    target = generate_variable_or_tuple()
    iter = generate_expression(max_depth=max_depth)
    body = generate_block(max_depth=max_depth)
    orelse = random.choice([generate_block(max_depth=max_depth), []])
    return ast.For(target, iter, body, orelse)
