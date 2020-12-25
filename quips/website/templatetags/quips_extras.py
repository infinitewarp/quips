import random

from django import template

from quips.quips.anonymize import obfuscate_name

register = template.Library()
register.filter("obfuscate_name", obfuscate_name)

GIPHY_HTML = (
    '<iframe src="//giphy.com/embed/{0}?html5=true&hideSocial=true" '
    'width="{1}" height="{2}" frameborder="0" class="giphy-embed" '
    'allowfullscreen=""></iframe>'
)
# TODO Make this configurable/DB-driven?
GIPHY_IDS = (
    ("LPn77YyDIqfhm", 480, 270),  # "You've Got Mail" Tom Hanks typing
    ("XsUtdIeJ0MWMo", 480, 360),  # Picard two-handed facepalm (The Offspring)
    ("52VjAeGgj78GY", 480, 377),  # Picard deal with it
    ("b1NpJFw89s7UA", 480, 355),  # Picard damn
    ("baDHsD0Bk3K5a", 480, 384),  # Picard damn you
    ("xSM46ernAUN3y", 480, 384),  # Jeremiah Johnson nod
    ("jhmjR9RZYS92M", 480, 384),  # Sisko frown
    ("TJawtKM6OCKkvwCIqX", 480, 354),  # Picard facepalm (The Drumhead)
    ("109Pz1wDYxNLmE", 480, 480),  # Picard wink
    ("10p704gIAGRN7i", 480, 360),  # Worf facepalm (DS9)
    ("wHBkzKahBgFEM1S4GE", 480, 360),  # Data laughing (Déjà Q)
    ("dmB5vD2t2gR8Y", 480, 360),  # Data laughing 2 (Déjà Q)
)
GIPHYS = [GIPHY_HTML.format(*values) for values in GIPHY_IDS]


@register.simple_tag
def random_error_giphy(*args, **kwargs):
    return random.choice(GIPHYS)
