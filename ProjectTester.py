import unittest
import myValidator


class MyTestCase(unittest.TestCase):
    def test_myValidation(self):
        def test_length_checker():
            test_lengths = ["test", "test_test"]
            for i in test_lengths:
                ## need to finish this
        def test_format_checker():
            test_emails = ["test.test@test.com", "test@test.com", "@test.com", "test.com", "@", "test", ".com"]
            # A list of seven different email formats, where the first two are valid and the remaining are invalid
            for i in range(2):  # First two emails are checked
                test_case = myValidator.Validator.format_checker(test_emails[1], 1)
                self.assertEqual(test_case, True)
                # The first two emails should return True since they are in the correct email form
            for i in range(2, 6):  # Rest of emails are checked
                test_case = myValidator.Validator.format_checker(test_emails[i], 1)
                self.assertEqual(test_case, False)
                # The last five emails should return False since they are not in the correct email form
        test_format_checker()


MyTestCase().test_myValidation()
