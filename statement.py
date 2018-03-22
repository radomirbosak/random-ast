import ast
import random

from expression import generate_expression, binary_ops
from variable import generate_variable, generate_variable_or_tuple
from literal import generate_string


def generate_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    targets = [generate_variable_or_tuple(max_depth=max_depth, ctx=ast.Store())]
    return ast.Assign(targets, value)


def generate_statement(max_depth=None):
    choices = [
        generate_assign,
        generate_annotated_assign,
        generate_augmented_assign,
        generate_raise,
        generate_assert,
    ]
    return random.choice(choices)(max_depth=max_depth)


def generate_annotated_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    target = generate_variable(max_depth=max_depth, ctx=ast.Store())
    annotation = generate_variable(max_depth=max_depth)
    return ast.AnnAssign(target, annotation, value, 1)


def generate_augmented_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    target = generate_variable(max_depth=max_depth, ctx=ast.Store())

    op = random.choice(binary_ops)()

    return ast.AugAssign(target, op, value)


def generate_raise(max_depth=None):
    exc = generate_variable()
    cause = random.choice([generate_variable(), None])
    return ast.Raise(exc, cause)


def generate_assert(max_depth=None):
    test = generate_expression(max_depth=max_depth)
    msg = random.choice([generate_string(), None])

    return ast.Assert(test, msg)
