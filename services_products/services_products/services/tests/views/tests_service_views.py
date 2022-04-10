from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services_products.accounts.models import Profile
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
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user,
        )
        return user, profile

    def __create_service(self, item, user):
        item = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        item.save()
        return item

    def test_list_services__when_there_are_existing_service__expect_success(self):
        user, profile = self.__create_user_profile()

        for service in range(5):
            self.__create_service(service, user)

        response = self.client.get(reverse('list services'))
        self.assertEqual(5, response.context['weekly'])

    def test_list_services__when_there_are_no_existing_services__expect_success(self):
        response = self.client.get(reverse('list services'))
        self.assertEqual(0, response.context['weekly'])

    def test_service_view__when_there_are_existing_services__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertTrue('The best service' in str(response.content))

    def test_service_view__when_there_are_no_existing_services__expect_success(self):
        response = self.client.get(reverse('service details', kwargs={'pk': 25}))
        self.assertEqual(404, response.status_code)

    def test_own_list_services__when_there_are_three_existing_services__expect_success(self):
        user, profile = self.__create_user_profile()

        for service in range(3):
            self.__create_service(service, user)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('view own services'))
        self.assertEqual(3, response.context['weekly'])

    def test_own_service_edit__when_there_are_existing_service__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertTrue('Edit' in str(response.content))

    def test_own_service_delete__when_there_are_existing_service__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertTrue('Delete' in str(response.content))

    def test_not_own_service_edit__when_there_are_existing_service__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertFalse('Edit' in str(response.content))

    def test_not_own_service_delete__when_there_are_existing_service__expect_success(self):
        user, profile = self.__create_user_profile()
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        response = self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.assertFalse('Delete' in str(response.content))