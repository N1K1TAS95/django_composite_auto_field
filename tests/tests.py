from unittest.mock import patch

from django.test import TestCase
from django.utils.timezone import now

from tests.models import TestModelA, TestModelB


class CompositeAutoFieldTestCase(TestCase):

    def test_auto_increment(self):
        """
        Test that the custom_code field auto increments properly.
        """
        # Create and save two instances of the test model
        test_model1 = TestModelA.objects.create()
        test_model2 = TestModelA.objects.create()

        # Check if the custom_code field values are different
        self.assertNotEqual(test_model1.custom_code, test_model2.custom_code)

    def test_prefix(self):
        """
        Test that the custom_code field has the correct prefix.
        """
        # Create an instance of the test model
        test_model = TestModelA.objects.create()

        # Check if the custom_code field starts with the correct prefix
        self.assertTrue(test_model.custom_code.startswith('AA'))

    def test_year_change(self):
        """
        Test that the custom_code field updates the year and resets the counter when the year changes.
        """
        # Create a model in the current year
        test_model_current_year = TestModelA()
        test_model_current_year.save()

        # Advance the current year by one year
        next_year = now().year + 1

        # Patch the current year to simulate year change
        with patch('django_composite_auto_field.fields.now') as mock_now:
            mock_now.return_value = now().replace(year=next_year)

            # Create a model in the next year
            test_model_next_year = TestModelA()
            test_model_next_year.save()

            # Check if the year in the custom_code field has been updated
            next_year_str = str(test_model_next_year.custom_code[2:4])
            self.assertEqual(next_year_str, str(next_year)[2:])

            # Check if the counter has been reset
            counter_current_year = int(test_model_current_year.custom_code[4:])
            counter_next_year = int(test_model_next_year.custom_code[4:])
            self.assertEqual(counter_current_year, counter_next_year)

    def test_zeros(self):
        """
        Test that the custom_code field has the correct number of zeros.
        """
        # Create and save an instance of the test model
        test_model = TestModelA.objects.create()

        # Check if the number of zeros is correct
        number_of_zeros = 4
        zeros = test_model.custom_code[4:4 + number_of_zeros]
        self.assertEqual(len(zeros), number_of_zeros)

    def test_prefix_variations(self):
        """
        Test that different models can have different prefixes.
        """
        test_model_a = TestModelA.objects.create()
        test_model_b = TestModelB.objects.create()

        # Check if the custom_code field starts with the correct prefixes
        self.assertTrue(test_model_a.custom_code.startswith('AA'))
        self.assertTrue(test_model_b.custom_code.startswith('BB'))

    def test_zeros_variations(self):
        """
        Test that different models can have a different number of zeros.
        """
        # Create and save instances of the test models
        test_model_a = TestModelA.objects.create()
        test_model_b = TestModelB.objects.create()

        number_of_zeros_a = 4
        number_of_zeros_b = 5

        # Extract the zeros from the custom_code fields of the models
        zeros_a = test_model_a.custom_code[4:4 + number_of_zeros_a]
        zeros_b = test_model_b.custom_code[2:2 + number_of_zeros_b]

        # Check if the number of zeros is correct for each model
        self.assertEqual(len(zeros_a), number_of_zeros_a)
        self.assertEqual(len(zeros_b), number_of_zeros_b)

    def test_custom_code_override(self):
        """
        Test that the custom_code field can be overridden with a custom value.
        """
        custom_code_value = 'AA230001'

        # Create and save an instance of the test model with a custom custom_code value
        test_model_a = TestModelA.objects.create(custom_code=custom_code_value)

        # Check if the custom_code field has the custom value
        self.assertEqual(test_model_a.custom_code, custom_code_value)

    def test_code_sequence(self):
        """
        Test that the custom_code field generates codes in the correct sequence.
        """
        # Create three models
        test_model_1 = TestModelA()
        test_model_1.save()
        test_model_2 = TestModelA()
        test_model_2.save()
        test_model_3 = TestModelA()
        test_model_3.save()

        # Extract the current year and the numeric parts of the generated codes
        current_year = str(now().year)[2:]
        num_1 = int(test_model_1.custom_code[4:])
        num_2 = int(test_model_2.custom_code[4:])
        num_3 = int(test_model_3.custom_code[4:])

        # Check that the prefixes and years are correct
        self.assertEqual(test_model_1.custom_code[:4], f'AA{current_year}')
        self.assertEqual(test_model_2.custom_code[:4], f'AA{current_year}')
        self.assertEqual(test_model_3.custom_code[:4], f'AA{current_year}')

        # Check that the numbers are in sequence
        self.assertEqual(num_2, num_1 + 1)
        self.assertEqual(num_3, num_2 + 1)
