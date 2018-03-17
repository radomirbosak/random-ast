#!/usr/bin/python3
import ast
import random

import astor

"""
compile_mode: exec, single, eval
"""

ops = [
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


def random_number():
    r = random.randrange(5)
    return ast.Num(r)

def random_binop():
    left = random_number()
    right = random_number()
    op = random.choice(ops)
    return ast.BinOp(left, getattr(ast, op)(), right)

rbop = random_binop()
p(rbop)

expr = ast.Expression(rbop)
ast.fix_missing_locations(expr)

back_code = astor.code_gen.to_source(expr)
print(back_code)

a = eval(compile(expr, '', 'eval'))
print(a)

