import ast

from words import generate_variable_name

def generate_variable(max_depth=None):
    name = generate_variable_name()
    return ast.Name(name, ast.Load())
