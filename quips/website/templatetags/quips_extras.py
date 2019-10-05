import random

from django import template
from memoize import memoize

register = template.Library()


@memoize(timeout=5)
def obfuscate_name(value, delimeter=" "):
    names = value.split(delimeter)

    def shuffle_word(word):
        if not word or len(word) < 3:
            return word
        if "-" in word:
            return obfuscate_name(word, delimeter="-")
        guts = list(word[1:-1])
        random.shuffle(guts)
        new_word = word[0] + "".join(guts) + word[-1]
        if new_word == word:
            # if shuffle didn't sufficiently randomize, just flip it
            new_word = word[0] + "".join(guts[::-1]) + word[-1]
        return new_word

    new_name = delimeter.join([shuffle_word(word) for word in names])
    return new_name


@register.filter(name="obfuscate_name")
def obfuscate_name_filter(value, delimeter=" "):
    """
    Wrap the memoized obfuscate_name function.

    For some mysterious reason, recent versions of Django *require* the
    filter function to have named arguments, and if you give a decorated
    function that just deals with *args, **kwargs, the template renderer
    thinks the target function accepts no arguments at all.
    """
    return obfuscate_name(value, delimeter)


# TODO Make this configurable/DB-driven?
GIPHYS = [
    '<iframe src="//giphy.com/embed/LPn77YyDIqfhm?html5=true&hideSocial=true" width="480" height="270" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/XsUtdIeJ0MWMo?html5=true&hideSocial=true" width="480" height="360" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/52VjAeGgj78GY?html5=true&hideSocial=true" width="480" height="377" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/b1NpJFw89s7UA?html5=true&hideSocial=true" width="480" height="355" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/baDHsD0Bk3K5a?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/xSM46ernAUN3y?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/oTiG8QJA2Kldm?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/jhmjR9RZYS92M?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
]


@register.simple_tag
def random_error_giphy(*args, **kwargs):
    return random.choice(GIPHYS)
