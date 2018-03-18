import random
import string


variable_letterset = set(string.ascii_lowercase)


def get_words():
    with open('/usr/share/dict/words', 'r') as fd:
        return [word.rstrip() for word in fd.readlines()]
words = get_words()


def generate_word():
    return random.choice(words)

def generate_variable_name():
    word = '!'
    while not set(word).issubset(variable_letterset):
        word = generate_word()
    return word
