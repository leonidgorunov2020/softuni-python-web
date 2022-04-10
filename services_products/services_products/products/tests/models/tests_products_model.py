from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services_products.accounts.models import Profile
from services_products.products.models import Product

UserModel = get_user_model()


class ProductTests(TestCase):
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
    VALID_PRODUCT_DETAILS = {
        'name': 'The best product',
        'type': Product.PLUGIN,
        'date_of_release': date.today(),
        'price': 35,
    }

    def __create_user_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user,
        )
        return user, profile

    def test_create_job_item_with_valid_data__expect_success(self):
        user, profile = self.__create_user_profile()
        product = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        product.save()
        response = self.client.get(reverse('product details', kwargs={'pk': product.pk}))
        self.assertEqual(200, response.status_code)
