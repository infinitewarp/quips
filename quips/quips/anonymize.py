import random
import time
from datetime import date

from django.core.cache import cache


def shuffle_word(word):
    if not word or len(word) < 3:
        return word
    if "-" in word:
        return obfuscate_name(word, delimeter="-")
    if len(word) == 3:
        # Very special case to swap second and third characters and preserve case.
        return (
            word[0]
            + (word[2].upper() if word[1].isupper() else word[2].lower())
            + (word[1].upper() if word[2].isupper() else word[1].lower())
        )
    guts = list(word[1:-1])
    # Rotate the seed daily for predictable name patterns.
    # Normally a bad idea, this is fine here since we don't need secure randomness.
    random.seed(time.mktime(date.today().timetuple()))
    random.shuffle(guts)
    random.seed()
    new_word = word[0] + "".join(guts) + word[-1]
    if new_word == word:
        # if shuffle didn't sufficiently randomize, just flip it
        new_word = word[0] + "".join(guts[::-1]) + word[-1]
    return new_word


def obfuscate_name(value, delimeter=" "):
    cache_key = f"obfuscate_name_{hash((value, delimeter))}"
    if new_name := cache.get(cache_key):
        return new_name
    names = value.split(delimeter)
    new_name = delimeter.join([shuffle_word(word) for word in names])
    cache.set(cache_key, new_name, 5)
    return new_name
