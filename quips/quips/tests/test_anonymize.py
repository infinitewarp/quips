from django.test import TestCase

from quips.quips import anonymize


class AnonymizeTest(TestCase):
    def assertWordIsShuffledTypically(self, word, shuffled):
        """Assert a word is shuffled, preserving first and last characters."""
        self.assertNotEqual(word, shuffled)
        self.assertEqual(word[0], shuffled[0])
        self.assertEqual(word[-1], shuffled[-1])

    def test_shuffle_word_long(self):
        """Test a reasonably long word is shuffled."""
        word = "Enterprise"
        shuffled = anonymize.shuffle_word(word)
        self.assertWordIsShuffledTypically(word, shuffled)

    def test_shuffle_word_tiny(self):
        """Test a tiny word does not is shuffled."""
        word = "Ro"
        shuffled = anonymize.shuffle_word(word)
        self.assertEqual(word, shuffled)

    def test_shuffle_word_three(self):
        """Test a three-character word is shuffled."""
        word = "Odo"
        expected = "Ood"
        shuffled = anonymize.shuffle_word(word)
        self.assertNotEqual(word, shuffled)
        self.assertEqual(shuffled, expected)

    def test_shuffle_word_three_case(self):
        """Test a three-character word is shuffled preserving case."""
        word = "MrE"
        expected = "MeR"
        shuffled = anonymize.shuffle_word(word)
        self.assertNotEqual(word, shuffled)
        self.assertEqual(shuffled, expected)

    def test_obfuscate_name(self):
        """Test the words are shuffled in a typical two-word name."""
        name = "Thomas Riker"
        obfuscated = anonymize.obfuscate_name(name)
        self.assertNotEqual(name, obfuscated)
        for word, obfuscated_word in zip(name.split(" "), obfuscated.split(" ")):
            self.assertWordIsShuffledTypically(word, obfuscated_word)
