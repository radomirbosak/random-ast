from statement import generate_statement
import random


MAX_STATEMENTS = 5


def generate_block(max_depth=None):
    choices = [
        generate_pure_block,
    ]

    return random.choice(choices)(max_depth=max_depth - 1)


def generate_pure_block(max_depth=None):
    num_statements = random.randrange(1, MAX_STATEMENTS)

    return [generate_statement(max_depth=max_depth) for _ in range(num_statements)]
