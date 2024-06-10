import unittest
import MyValidator


class MyTestCase(unittest.TestCase):
    def test_myValidation(self):
        def test_length_checker():
            test_lengths = ["test", "test_test"]  # Two test cases to check
            for i in test_lengths:
                test_case = MyValidator.Validator.length_checker(i, len(i), 1)
                self.assertEqual(test_case, True)  # Check that true is returned since, len(info) == size

        def test_format_checker():
            test_emails = ["test.test@test.com", "test@test.com", "@test.com", "test.com", "@", "test", ".com"]
            # A list of seven different email formats, where the first two are valid and the remaining are invalid
            for i in range(2):  # First two emails are checked
                test_case = MyValidator.Validator.format_checker(test_emails[1], 1)
                self.assertEqual(test_case, True)
                # The first two emails should return True since they are in the correct email form
            for i in range(2, 7):  # Rest of emails are checked
                test_case = MyValidator.Validator.format_checker(test_emails[i], 1)
                self.assertEqual(test_case, False)
                # The last five emails should return False since they are not in the correct email form

        def test_data_type_checker():
            test_data = ["A", "10", 10, 10.0, False]
            data_types = [str, str, int, float, bool]
            # A list of five data types, which we will be checking
            # First two data types are strings, third is an int, fourth is a float, fifth is a bool
            for i in range(5):
                test_case = MyValidator.Validator.data_type_checker(test_data[i], data_types[i], 1)
                self.assertEqual(test_case, True)
                #  Check that each test data is the correct data type

        test_length_checker()  # Run the length checker test
        test_format_checker()  # Run the format checker test
        test_data_type_checker()  # Run the data type checker test
