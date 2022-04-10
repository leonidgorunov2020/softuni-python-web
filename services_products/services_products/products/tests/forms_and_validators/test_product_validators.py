from unittest import TestCase

from django.core.exceptions import ValidationError

from services_products.products.validators import MaxFileSizeInMbValidator


class RandomFile:
    size = 6


class RandomImage:
    file = RandomFile()


class MaxFileSizeTest(TestCase):
    def test_test_when_user_file_is_larger__expect_error(self):
        validator = MaxFileSizeInMbValidator(0.000001)
        file = RandomImage()

        with self.assertRaises(ValidationError) as context:
            validator(file)

        self.assertIsNotNone(context.exception)

    def test_test_when_user_file_is_less__expect_to_do_nothing(self):
        validator = MaxFileSizeInMbValidator(1)
        file = RandomImage()

        validator(file)

