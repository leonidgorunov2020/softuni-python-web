from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services_products.accounts.models import Profile
from services_products.jobs.models import Job

UserModel = get_user_model()


class JobsTests(TestCase):
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

    def test_list_job__when_there_are_existing_jobs__expect_success(self):
        user, profile = self.__create_user_profile()

        def create_jobs(item):
            item = Job.objects.create(
                **self.VALID_JOB_DETAILS,
                user=user
            )
            item.save()

        for job in range(5):
            create_jobs(job)

        response = self.client.get(reverse('list jobs'))
        self.assertEqual(5, response.context['part_time'])

    def test_list_job__when_there_are_no_existing_job__expect_success(self):
        response = self.client.get(reverse('list jobs'))
        self.assertEqual(0, response.context['part_time'])

    def test_job_view__when_there_are_existing_job__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertTrue('Top Job' in str(response.content))

    def test_job_view__when_there_are_no_existing_job__expect_success(self):
        response = self.client.get(reverse('job details', kwargs={'pk': 5}))
        self.assertEqual(404, response.status_code)

    def test_own_list_job__when_there_are_three_existing_jobs__expect_success(self):
        user, profile = self.__create_user_profile()

        def create_jobs(item):
            item = Job.objects.create(
                **self.VALID_JOB_DETAILS,
                user=user
            )
            item.save()

        for job in range(3):
            create_jobs(job)

        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('view own jobs'))
        self.assertEqual(3, response.context['part_time'])

    def test_own_job_edit__when_there_are_existing_job__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertTrue('Edit' in str(response.content))

    def test_own_job_delete__when_there_are_existing_job__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertTrue('Delete' in str(response.content))

    def test_not_own_job_delete__when_there_are_existing_job__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertFalse('Delete' in str(response.content))

    def test_not_own_job_edit__when_there_are_existing_job__expect_success(self):
        user, profile = self.__create_user_profile()
        job = Job.objects.create(
            **self.VALID_JOB_DETAILS,
            user=user
        )
        job.save()
        response = self.client.get(reverse('job details', kwargs={'pk': job.pk}))
        self.assertFalse('Edit' in str(response.content))
