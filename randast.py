#!/usr/bin/python3
import ast
import random

import astor

from expression import generate_expression
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
    # print AST representation
    rbop = generate_expression(max_depth=2)
    p(rbop)

    expr = ast.Expression(rbop)
    ast.fix_missing_locations(expr)

    # print source
    back_code = astor.code_gen.to_source(expr)
    print(back_code)

    # print evaluated result
    a = eval(compile(expr, '', 'eval'))
    print(a)

if __name__ == '__main__':
    main()
