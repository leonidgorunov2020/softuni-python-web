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

    def test_list_product_page__when_there_are_five_existing_jobs__expect_success(self):
        user, profile = self.__create_user_profile()

        def create_product(item):
            item = Product.objects.create(
                **self.VALID_PRODUCT_DETAILS,
                user=user
            )
            item.save()

        for product in range(5):
            create_product(product)

        response = self.client.get(reverse('list products'))
        self.assertEqual(5, response.context['plugins'])

    def test_list_product_page__when_there_are_no_existing_jobs__expect_success(self):
        response = self.client.get(reverse('list products'))
        self.assertEqual(0, response.context['plugins'])

    def test_own_product_edit__when_there_are_existing_product__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        job.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('product details', kwargs={'pk': job.pk}))
        self.assertTrue('Edit' in str(response.content))

    def test_own_product_delete__when_there_are_existing_product__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        job.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('product details', kwargs={'pk': job.pk}))
        self.assertTrue('Delete' in str(response.content))


    def test_not_own_product_edit__when_there_are_existing_product__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        job.save()
        response = self.client.get(reverse('product details', kwargs={'pk': job.pk}))
        self.assertFalse('Edit' in str(response.content))

    def test_not_own_product_delete__when_there_are_existing_product__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        job.save()
        response = self.client.get(reverse('product details', kwargs={'pk': job.pk}))
        self.assertFalse('Delete' in str(response.content))
