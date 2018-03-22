#!/usr/bin/python3
import ast
import random

import astor

from expression import generate_expression
from statement import generate_statement
from literal import generate_list
"""
compile_mode: exec, single, eval
"""

bin_ops = [
    'Add',
    'BitAnd',
    'BitOr',
    'BitXor',
    'Div',
    'FloorDiv',
    'LShift',
    'MatMult',
    'Mod',
    'Mult',
    'Pow',
    'RShift',
    'Sub',
    # 'operator'
]


def p(astnode):
    print(ast.dump(astnode))


def pp(string):
    print(astor.dump_tree(ast.parse(string)))


def main():
    for _ in range(5):
        expr = generate_statement(max_depth=2)
        back_code = astor.code_gen.to_source(expr)
        print(back_code)

if __name__ == '__main__':
    main()
