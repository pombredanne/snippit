from django.test import TestCase
from account.validators import username_re


class UsernameRegexTestCase(TestCase):
    """
    Username Regex Test Cases
    """

    def test_short_username(self):
        """
        Should be between 4 and 25
        """
        self.assertNotRegexpMatches('aaa', username_re)

    def test_long_username(self):
        """
        Should be between 4 and 25
        """
        self.assertNotRegexpMatches('a' * 30, username_re)

    def test_valid_username(self):
        """
        Valid username
        """
        self.assertRegexpMatches('snippit', username_re)

    def test_invalid_character(self):
        """
        '?' invalid character
        """
        self.assertNotRegexpMatches('snippit?', username_re)