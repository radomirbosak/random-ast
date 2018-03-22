import ast
import random

from words import generate_variable_name
from variable import generate_variable
from literal import generate_literal, MAX_LIST_LENGTH

MAX_ARGS_LENGTH = 3

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
bool_ops = [ast.Or, ast.And]
comparisons = [
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
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
            generate_comparison,
            generate_function_call,
            generate_inline_if,
            generate_attribute,
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
    op = random.choice(bool_ops)
    length = max(2, random.randrange(0, MAX_LIST_LENGTH))

    values = [generate_expression(max_depth=max_depth - 1) for _ in range(length)]
    return ast.BoolOp(op(), values)


def generate_comparison(max_depth=None):
    length = max(2, random.randrange(0, MAX_LIST_LENGTH))

    ops = [op() for op in random.choices(comparisons, k=length - 1)]
    left, *comparators = [generate_expression(max_depth=max_depth - 1) for _ in range(length)]

    return ast.Compare(left, ops, comparators)


def _generate_keyword(max_depth=None, starred=False):
    argname = generate_variable_name() if not starred else None
    value = generate_expression(max_depth=max_depth - 1)
    return ast.keyword(arg=argname, value=value)


def generate_function_call(max_depth=None):
    args_len = random.randrange(MAX_ARGS_LENGTH)
    kwargs_len = random.randrange(MAX_ARGS_LENGTH)

    starred_args = random.choice([False, True])
    starred_kwargs = random.choice([False, True])

    args = [generate_expression(max_depth=max_depth - 1) for _ in range(args_len)]
    if starred_args:
        starred = ast.Starred(generate_expression(max_depth=max_depth - 1), ast.Load)
        args.append(starred)

    kwargs = [_generate_keyword(max_depth=max_depth) for _ in range(kwargs_len)]
    if starred_kwargs:
        kwargs.append(_generate_keyword(max_depth=max_depth, starred=True))

    name = generate_variable()
    return ast.Call(func=name, args=args, keywords=kwargs)


def generate_inline_if(max_depth=None):
    test = generate_expression(max_depth=max_depth - 1)
    body = generate_expression(max_depth=max_depth - 1)
    orelse = generate_expression(max_depth=max_depth - 1)

    return ast.IfExp(test, body, orelse)


def generate_attribute(max_depth=None):
    value = generate_expression(max_depth=max_depth - 1)
    attr = generate_variable_name()

    return ast.Attribute(value, attr, ast.Load())
