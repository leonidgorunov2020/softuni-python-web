from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services_products.services.models import Service

UserModel = get_user_model()


class ServiceTests(TestCase):
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
    VALID_SERVICE_DETAILS = {
        'name': 'The best service',
        'cycle': Service.WEEKLY,
        'date_of_publish': date.today(),
        'fee': 35,
    }

    def __create_user_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user,
        )
        return user, profile

    def test_create_service_item_with_valid_data__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertEqual(200, response.status_code)