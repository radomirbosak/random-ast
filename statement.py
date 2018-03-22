import ast
import random

from expression import generate_expression, binary_ops, generate_subscript, generate_attribute
from variable import generate_variable, generate_variable_or_tuple
from literal import generate_string
from words import generate_variable_name


def generate_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    targets = [generate_variable_or_tuple(max_depth=max_depth, ctx=ast.Store())]
    return ast.Assign(targets, value)


def generate_statement(max_depth=None):
    choices = [
        generate_assign,
        generate_annotated_assign,
        generate_augmented_assign,
        generate_raise,
        generate_assert,
        generate_delete,
        generate_pass,
        generate_import,
        generate_import_from,
    ]
    return random.choice(choices)(max_depth=max_depth)


def generate_annotated_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    target = generate_variable(max_depth=max_depth, ctx=ast.Store())
    annotation = generate_variable(max_depth=max_depth)
    return ast.AnnAssign(target, annotation, value, 1)


def generate_augmented_assign(max_depth=None):
    value = generate_expression(max_depth=max_depth)
    target = generate_variable(max_depth=max_depth, ctx=ast.Store())

    op = random.choice(binary_ops)()

    return ast.AugAssign(target, op, value)


def generate_raise(max_depth=None):
    exc = generate_variable()
    cause = random.choice([generate_variable(), None])
    return ast.Raise(exc, cause)


def generate_assert(max_depth=None):
    test = generate_expression(max_depth=max_depth)
    msg = random.choice([generate_string(), None])

    return ast.Assert(test, msg)

def generate_delete(max_depth=None):
    num_nodes = random.randrange(1, 4)

    choices = [
        generate_variable,
        generate_attribute,
        generate_subscript,
    ]

    targets = [tar(max_depth=max_depth, ctx=ast.Store()) for tar in random.choices(choices, k=num_nodes)]

    return ast.Delete(targets)


def generate_pass(max_depth=None):
    return ast.Pass()


def _generate_alias():
    name = generate_variable_name()
    asname = random.choice([generate_variable_name(), None])
    return ast.alias(name, asname)


def _generate_module_name():
    num_parts = random.randrange(1, 4)
    names = [generate_variable_name() for _ in range(num_parts)]
    return '.'.join(names)


def generate_import(max_depth=None):
    num_names = random.randrange(1, 4)
    names = [_generate_alias() for _ in range(num_names)]

    return ast.Import(names)


def generate_import_from(max_depth=None):
    module = _generate_module_name()
    level = random.randrange(3)
    num_names = random.randrange(1, 4)
    names = [_generate_alias() for _ in range(num_names)]

    return ast.ImportFrom(module, names, level)
