import random

from django import template

from quips.quips.anonymize import obfuscate_name

register = template.Library()
register.filter("obfuscate_name", obfuscate_name)

# TODO Make this configurable/DB-driven?
GIPHYS = [
    '<iframe src="//giphy.com/embed/LPn77YyDIqfhm?html5=true&hideSocial=true" width="480" height="270" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/XsUtdIeJ0MWMo?html5=true&hideSocial=true" width="480" height="360" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/52VjAeGgj78GY?html5=true&hideSocial=true" width="480" height="377" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/b1NpJFw89s7UA?html5=true&hideSocial=true" width="480" height="355" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/baDHsD0Bk3K5a?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/xSM46ernAUN3y?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/jhmjR9RZYS92M?html5=true&hideSocial=true" width="480" height="384" frameborder="0" class="giphy-embed" allowfullscreen=""></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/gLvBksqQE5j60Ud8R7?html5=true&hideSocial=true" width="480" height="266" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/TJawtKM6OCKkvwCIqX?html5=true&hideSocial=true" width="480" height="354" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/109Pz1wDYxNLmE?html5=true&hideSocial=true" width="480" height="480" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/10p704gIAGRN7i?html5=true&hideSocial=true" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/wHBkzKahBgFEM1S4GE?html5=true&hideSocial=true" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
    '<iframe src="//giphy.com/embed/dmB5vD2t2gR8Y?html5=true&hideSocial=true" width="480" height="360" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>',  # noqa
]


@register.simple_tag
def random_error_giphy(*args, **kwargs):
    return random.choice(GIPHYS)
