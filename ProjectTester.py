import unittest
import MyValidator


class MyTestCase(unittest.TestCase):
    def test_myValidation(self):
        def test_length_checker():
            test_lengths = ["test", "test_test"]  # Two test cases to check
            for i in test_lengths:
                test_case = myValidator.Validator.length_checker(i, len(i), 1)
                self.assertEqual(test_case, True)  # Check that true is returned since, len(info) == size

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

        def run_tests():
            test_length_checker()  # Run the length checker test
            test_format_checker()  # Run the format checker test
        run_tests()
