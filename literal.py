import ast
import random


def get_words():
    with open('/usr/share/dict/words', 'r') as fd:
        return [word.rstrip() for word in fd.readlines()]
words = get_words()


def generate_num():
    n = random.randrange(10)
    return ast.Num(n)


def generate_string():
    word = random.choice(words)
    return ast.Str(word)


def generate_ellipsis():
    return ast.Ellipsis()


def generate_name_constant():
    constant = random.choice([True, False, None])
    return ast.NameConstant(constant)


def generate_literal():
    choices = [
        generate_num,
        generate_string,
        generate_ellipsis,
        generate_name_constant,
    ]
    return random.choice(choices)()
