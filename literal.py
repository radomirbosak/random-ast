import ast
import random

from words import generate_word


def generate_num():
    n = random.randrange(10)
    return ast.Num(n)


def generate_string():
    return ast.Str(generate_word())


def generate_bytes():
    seq = generate_word().encode('utf-8')
    return ast.Bytes(seq)


def generate_ellipsis():
    return ast.Ellipsis()


def generate_name_constant():
    constant = random.choice([True, False, None])
    return ast.NameConstant(constant)


def generate_literal():
    choices = [
        generate_num,
        generate_string,
        generate_bytes,
        generate_ellipsis,
        generate_name_constant,
    ]
    return random.choice(choices)()
