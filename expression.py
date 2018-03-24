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
            generate_subscript,
            generate_comprehension,
            generate_lambda,
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


def generate_attribute(max_depth=None, ctx=ast.Load()):
    value = generate_expression(max_depth=max_depth - 1)
    attr = generate_variable_name()

    return ast.Attribute(value, attr, ctx)


def _generate_index_slice(max_depth=None):
    return ast.Index(generate_expression(max_depth=max_depth - 1))


def _generate_simple_slice(max_depth=None):
    upper = generate_expression(max_depth=max_depth - 1)
    lower = generate_expression(max_depth=max_depth - 1)
    step = generate_expression(max_depth=max_depth - 1)

    return ast.Slice(lower=lower, upper=upper, step=step)


def _generate_extended_slice(max_depth=None):
    choices = [
        _generate_index_slice,
        _generate_simple_slice,
    ]
    dims_len = random.randrange(2, 4)
    dims = [sl(max_depth=max_depth - 1) for sl in random.choices(choices, k=dims_len)]
    return ast.ExtSlice(dims)


def generate_subscript(max_depth=None, ctx=ast.Load()):
    value = generate_expression(max_depth=max_depth)
    choices = [
        _generate_index_slice,
        _generate_simple_slice,
        _generate_extended_slice,
    ]
    slice_gen = random.choice(choices)
    sl = slice_gen(max_depth=max_depth)
    return ast.Subscript(value=value, slice=sl, ctx=ctx)


def _generate_comprehension(max_depth=None):
    target = generate_variable(max_depth=max_depth - 1)
    iterable = generate_expression(max_depth=max_depth - 1)

    ifs = [generate_expression(max_depth=max_depth - 1)]

    return ast.comprehension(target=target, iter=iterable, ifs=ifs)


def generate_comprehension(max_depth=None):
    num_generators = random.choice([1, 1, 1, 2])
    generators = [_generate_comprehension(max_depth=max_depth) for _ in range(num_generators)]

    compr_class = random.choice([
        ast.ListComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.DictComp,
    ])

    if compr_class is ast.DictComp:
        key = generate_expression(max_depth=max_depth - 1)
        value = generate_expression(max_depth=max_depth - 1)
        return compr_class(key=key, value=value, generators=generators)

    # all other comprehensions
    elt = generate_expression(max_depth=max_depth - 1)
    return compr_class(elt=elt, generators=generators)

def generate_lambda(max_depth=None):
    from function_class import _generate_arguments
    args = _generate_arguments(max_depth=max_depth)
    body = generate_expression(max_depth=max_depth - 1)
    return ast.Lambda(args, body)
