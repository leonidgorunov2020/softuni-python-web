from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services_products.accounts.models import WebUser, Profile
from services_products.jobs.models import Job
from services_products.products.models import Product
from services_products.services.models import Service

UserModel = get_user_model()
class TestSuccessfulLogin(TestCase):
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

    ANOTHER_VALID_USER_CREDENTIALS = {
        'username': 'pesho',
        'password': 'pesho123'
    }
    ANOTHER_VALID_PROFILE_CREDENTIALS = {
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
        'picture': 'http://googe.com/pic.jpg',
        'date_of_birth': date(2022, 1, 10),
        'personal_info': '',
        'email': '',
        'gender': 'Male'
    }
    VALID_PRODUCT_DETAILS = {
        'name': 'product_one',
        'type': Product.TEMPLATE,
        'date_of_release': date.today(),
        'price': 100
    }
    VALID_SERVICE_DETAILS = {
        'name': 'service_one',
        'cycle': Service.MONTHLY,
        'date_of_publish': date.today(),
        'fee': 100
    }

    VALID_JOB_DETAILS = {
        'title': 'Top Job',
        'job_types': Job.PART_TIME,
        'job_responsibilities': Job.SUPPORT,
        'date_of_publish': date.today(),
        'monthly_salary': 5000,
    }
    def __create_user_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user,
        )
        return user, profile

    def __create_another_user_profile(self):
        another_user = UserModel.objects.create_user(**self.ANOTHER_VALID_USER_CREDENTIALS)
        another_profile = Profile.objects.create(
            **self.ANOTHER_VALID_PROFILE_CREDENTIALS,
            user=another_user,
        )
        return another_user, another_profile

    def test_get_correct_template(self):
        response = self.client.get(reverse('login user'))
        self.assertTemplateUsed('accounts/login_page.html')

    def test_get_correct_profile_view_template_with_invalid_user__expect_404(self):
        response = self.client.get(reverse('profile view', kwargs={
            'pk': 123
        }))

        self.assertEqual(404, response.status_code)

    def test_get_correct_profile_view_template_with_valid_user__expect_success(self):
        user, profile = self.__create_user_profile()
        self.client.get(reverse('profile view', kwargs={
            'pk': profile.pk
        }))
        self.assertTemplateUsed('accounts/profile_view.html')

    def test_login_page_no_authentication_attempt(self):
        response = self.client.post(
            reverse('login user')
        )
        self.assertEqual(response.status_code, 200)

    def test_login_page_with_valid_user(self):
        user = WebUser.objects.create(username='ivan')
        user.set_password('ivan')
        user.save()

        logged_in = self.client.login(username='ivan', password='ivan')
        self.assertEqual(logged_in, True)


    def test_login_page_with_invalid_user(self):
        user = WebUser.objects.create(username='ivan')
        user.set_password('ivan')
        user.save()

        logged_in = self.client.login(username='ivan', password='ivan123')
        self.assertNotEqual(logged_in, True)

    def test_login_page_with_authenticated_user(self):
        user = WebUser.objects.create(username='ivan')
        user.set_password('ivan')
        user.save()

        logged_in = self.client.login(username='ivan', password='ivan')
        response = self.client.post(
            reverse('login user'),
        )
        expected_url = reverse('show index')
        self.assertRedirects(response, expected_url)

    def test_when_user_is_account_owner__expect_success(self):
        user, profile = self.__create_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile view', kwargs={'pk': profile.pk}))
        self.assertTrue(response.context['is_owner'])


    def test_when_user_is_not_account_owner__expect_fail(self):
        _, profile = self.__create_user_profile()
        self.client.login(**self.ANOTHER_VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile view', kwargs={'pk': profile.pk}))
        self.assertFalse(response.context['is_owner'])

    def test_last_viewed_products_if_viewed_product_exists__expect_success(self):
        user, profile = self.__create_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        product = Product.objects.create(
            **self.VALID_PRODUCT_DETAILS,
            user=user
        )
        product.save()
        self.client.get(reverse('product details', kwargs={'pk': product.pk}))
        self.client.get('last viewed product', kwargs={'pk', profile.pk})
        self.assertEqual(1, self.client.session['last_viewed_product'])


    def test_last_viewed_service_if_viewed_service_exists__expect_success(self):
        user, profile = self.__create_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        service = Service.objects.create(
            **self.VALID_SERVICE_DETAILS,
            user=user
        )
        service.save()
        self.client.get(reverse('service details', kwargs={'pk': service.pk}))
        self.client.get('last viewed product', kwargs={'pk', profile.pk})
        self.assertEqual(1, self.client.session['last_viewed_service'])

    def test_last_viewed_job_if_viewed_job_exists__expect_success(self):
        user, profile = self.__create_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.client.get('last viewed product', kwargs={'pk', profile.pk})
        self.assertEqual(1, self.client.session['last_viewed_job'])


