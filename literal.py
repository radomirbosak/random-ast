import ast
import random

from words import generate_word


def generate_num(max_depth=None):
    n = random.randrange(10)
    return ast.Num(n)


def generate_string(max_depth=None):
    return ast.Str(generate_word())


def generate_bytes(max_depth=None):
    seq = generate_word().encode('utf-8')
    return ast.Bytes(seq)


def generate_ellipsis(max_depth=None):
    return ast.Ellipsis()


def generate_name_constant(max_depth=None):
    constant = random.choice([True, False, None])
    return ast.NameConstant(constant)


def generate_literal(max_depth=None):
    choices = [
        generate_num,
        generate_string,
        generate_bytes,
        generate_ellipsis,
        generate_name_constant,
    ]
    return random.choice(choices)(max_depth=max_depth)
