#!/usr/bin/python3
import ast
import random

import astor

from literal import generate_literal
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


def random_binop():
    left = generate_literal()
    right = generate_literal()
    op = random.choice(bin_ops)
    return ast.BinOp(left, getattr(ast, op)(), right)


def main():
    # print AST representation
    rbop = random_binop()
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
