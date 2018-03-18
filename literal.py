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


def generate_literal():
    choices = ['num', 'str']
    choice = random.choice(choices)
    if choice == 'num':
        return generate_num()
    elif choice == 'str':
        return generate_string()
    else:
        raise NotImplementedError
