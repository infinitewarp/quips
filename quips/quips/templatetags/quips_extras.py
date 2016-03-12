import codecs
import random

from django import template
from memoize import memoize


@memoize(timeout=5)
def obfuscate_name(value):
    names = value.split(' ')

    def shuffle_word(word):
        if not word or len(word) < 3:
            return word
        guts = list(word[1:-1])
        random.shuffle(guts)
        new_word = word[0] + ''.join(guts) + word[-1]
        if new_word == word:
            # if shuffle didn't sufficiently randomize, just flip it
            new_word = word[0] + ''.join(guts[::-1]) + word[-1]
        return new_word

    new_name = ' '.join([shuffle_word(word) for word in names])
    return new_name


@memoize()
def rot13_name(value):
    names = value.split(' ')

    def shuffle_word(word):
        if not word or len(word) < 3:
            return word
        guts = word[1:-1]
        return word[0] + codecs.encode(guts, 'rot13') + word[-1]

    new_name = ' '.join([shuffle_word(word) for word in names])
    return new_name


register = template.Library()
register.filter('obfuscate_name', obfuscate_name)
register.filter('rot13_name', rot13_name)
