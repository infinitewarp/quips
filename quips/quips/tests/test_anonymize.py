from django.test import TestCase

import quips.quips.anonymize


class AnonymizeTest(TestCase):
    def test_shuffle_word_long(self):
        """Test a reasonably long word is shuffled."""
        word = "Enterprise"
        shuffled = quips.quips.anonymize.shuffle_word(word)
        self.assertNotEqual(word, shuffled)
        self.assertEqual(word[0], shuffled[0])
        self.assertEqual(word[-1], shuffled[-1])

    def test_shuffle_word_tiny(self):
        """Test a tiny word does not is shuffled."""
        word = "Ro"
        shuffled = quips.quips.anonymize.shuffle_word(word)
        self.assertEqual(word, shuffled)

    def test_shuffle_word_three(self):
        """Test a three-character word is shuffled."""
        word = "Odo"
        expected = "Ood"
        shuffled = quips.quips.anonymize.shuffle_word(word)
        self.assertNotEqual(word, shuffled)
        self.assertEqual(shuffled, expected)

    def test_shuffle_word_three_case(self):
        """Test a three-character word is shuffled preserving case."""
        word = "MrE"
        expected = "MeR"
        shuffled = quips.quips.anonymize.shuffle_word(word)
        self.assertNotEqual(word, shuffled)
        self.assertEqual(shuffled, expected)
