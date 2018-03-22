import ast
import random

from words import generate_variable_name
from variable import generate_variable_or_tuple
from expression import generate_expression
from statement import generate_statement


MAX_STATEMENTS = 5


def generate_block(max_depth=None):
    num_statements = random.randrange(1, MAX_STATEMENTS)
    choices = [
        generate_statement,
        generate_statement,
        generate_statement,
        generate_statement,
    ]
    if max_depth >= 1:
        choices += [
            generate_if,
            generate_for,
            generate_while,
            generate_try,
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


def generate_while(max_depth=None):
    test = generate_expression(max_depth=max_depth)
    body = generate_block(max_depth=max_depth)
    orelse = random.choice([generate_block(max_depth=max_depth), []])
    return ast.While(test, body, orelse)


def _generate_except_handler(max_depth=None):
    type = generate_variable_or_tuple()
    name = random.choice([generate_variable_name(), None])
    body = generate_block(max_depth=max_depth)

    return ast.ExceptHandler(type, name, body)


def generate_try(max_depth=None):
    body = generate_block(max_depth=max_depth)
    num_handlers = random.randrange(1, 3)
    handlers = [_generate_except_handler(max_depth=max_depth) for _ in range(num_handlers)]
    orelse = random.choice([generate_block(max_depth=max_depth), []])
    finalbody = random.choice([generate_block(max_depth=max_depth), []])
    return ast.Try(body, handlers, orelse, finalbody)
