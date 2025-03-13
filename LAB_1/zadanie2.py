import re
import unittest

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


class TestValidateEmail(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(validate_email("test@przyklad.pl"))
        self.assertTrue(validate_email("uzytkownik.nazwa+tag@przyklad.com"))
        self.assertTrue(validate_email("uzytkownik_nazwa@przyklad.edu.pl"))
        self.assertTrue(validate_email("uzytkownik-nazwa@przyklad.org"))

    def test_invalid_emails(self):
        self.assertFalse(validate_email("zwyklyadres"))
        self.assertFalse(validate_email("@braknazwyuzytkownika.pl"))
        self.assertFalse(validate_email("uzytkownik@.pl"))
        self.assertFalse(validate_email("uzytkownik@pl"))
        self.assertFalse(validate_email("uzytkownik@.pl."))
        self.assertFalse(validate_email("uzytkownik@-przyklad.pl"))
        self.assertFalse(validate_email("uzytkownik@przyklad..pl"))

if __name__ == '__main__':
    unittest.main()