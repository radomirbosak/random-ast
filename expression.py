import ast
import random

from variable import generate_variable
from literal import generate_literal, MAX_LIST_LENGTH

unary_ops = [ast.UAdd, ast.USub, ast.Not, ast.Invert]
binary_ops = [
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.MatMult,
]


def generate_expression(max_depth=None):
    choices = [
        generate_variable,
        generate_literal,
    ]
    if max_depth >= 1:
        choices += [
            generate_unary_op,
            generate_binary_op,
            generate_bool_op,
        ]

    return random.choice(choices)(max_depth=max_depth)


def generate_unary_op(max_depth=None):
    value = generate_expression(max_depth=max_depth - 1)
    op = random.choice(unary_ops)
    return ast.UnaryOp(op(), value)


def generate_binary_op(max_depth=None):
    left = generate_expression(max_depth=max_depth - 1)
    right = generate_expression(max_depth=max_depth - 1)
    op = random.choice(binary_ops)
    return ast.BinOp(left, op(), right)


def generate_bool_op(max_depth=None):
    op = random.choice([ast.Or, ast.And])
    length = random.randrange(MAX_LIST_LENGTH)

    values = [generate_expression(max_depth=max_depth - 1) for _ in range(length)]
    return ast.BoolOp(op(), values)
