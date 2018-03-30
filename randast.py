#!/usr/bin/env python3

import ast
import random

import astor

from expression import generate_expression
from statement import generate_statement
from control_flow import generate_block
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
    for module_idx in range(1):
        expr = generate_block(max_depth=3)
        if isinstance(expr, list):
            expr = ast.Module(body=expr)
        back_code = astor.code_gen.to_source(expr)
        print(f'# Module {module_idx}:')
        print(back_code)
        print()


if __name__ == '__main__':
    main()
