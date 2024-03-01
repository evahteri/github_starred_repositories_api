import unittest
import string
from services.random_string_generator import RandomStringGenerator


class TestRandomStringGenerator(unittest.TestCase):
    def setUp(self):
        self.random_string_generator = RandomStringGenerator()

    def test_random_string_length_10(self):
        """Test that the length of the random string is correct
        """
        length = 10
        random_string = self.random_string_generator.generate_random_string(
            length)
        self.assertEqual(len(random_string), length)

    def test_random_string_different_between_runs(self):
        """Test that the algorithm generates different strings on different runs
        """
        length = 10
        random_string_1 = self.random_string_generator.generate_random_string(
            length)
        random_string_2 = self.random_string_generator.generate_random_string(
            length)
        self.assertNotEqual(random_string_1, random_string_2)

    def test_random_string_content(self):
        """Test that the random string contains only letters and digits
        """
        length = 10
        random_string = self.random_string_generator.generate_random_string(
            length)
        self.assertTrue(all(c in string.ascii_letters +
                        string.digits for c in random_string))

    def test_random_string_negative_or_zero_length(self):
        """Test that the algorithm raises a ValueError for negative or zero length
        """
        length = 0
        with self.assertRaises(ValueError):
            self.random_string_generator.generate_random_string(length)
