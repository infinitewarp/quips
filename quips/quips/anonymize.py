import random

from memoize import memoize


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
    random.shuffle(guts)
    new_word = word[0] + "".join(guts) + word[-1]
    if new_word == word:
        # if shuffle didn't sufficiently randomize, just flip it
        new_word = word[0] + "".join(guts[::-1]) + word[-1]
    return new_word


@memoize(timeout=5)
def obfuscate_name(value, delimeter=" "):
    names = value.split(delimeter)

    new_name = delimeter.join([shuffle_word(word) for word in names])
    return new_name
