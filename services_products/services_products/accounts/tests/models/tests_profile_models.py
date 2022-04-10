from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from services_products.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'ivan',
        'password': 'ivan123'
    }
    VALID_PROFILE_CREDENTIALS = {
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'picture': 'http://googe.com/pic.jpg',
        'date_of_birth': date(2022, 1, 10),
        'personal_info': '',
        'email': '',
        'gender': 'Male'
    }

    INVALID_USER_CREDENTIALS = {
        'username': 'ivan',
        'password': 'ivan123'
    }
    INVALID_PROFILE_CREDENTIALS = {
        'last_name': 'Ivanov',
        'picture': 'http://googe.com/pic.jpg',
        'date_of_birth': date(2022, 1, 10),
        'personal_info': '',
        'email': '',
        'gender': 'Male'
    }

    def __create_user_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user,
        )
        return user, profile

    def __create_invalid_user_profile(self):
        invalid_user = UserModel.objects.create_user(**self.INVALID_USER_CREDENTIALS)
        invalid_profile = Profile.objects.create(
            **self.INVALID_PROFILE_CREDENTIALS,
            user=invalid_user,
        )
        return invalid_user, invalid_profile

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user, profile = self.__create_user_profile()
        self.assertIsNotNone(profile.pk)

    def test_profile_create__invalid_details__expect_fail(self):
        invalid_user, invalid_profile = self.__create_user_profile()
        self.assertIsNotNone(invalid_profile.pk)
