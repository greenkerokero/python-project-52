from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from task_manager.statuses.models import Status


class StatusTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        translation.activate('en')
        self.user = get_user_model().objects.get(pk=10001)
        self.password = 'Strongpass1!'
        self.user.set_password(self.password)
        self.user.save()
        self.status = Status.objects.get(pk=20001)

    def test_status_index(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:index'))
        expected_statuses = Status.objects.all()

        statuses_in_context = response.context['status_list']
        self.assertEqual(len(statuses_in_context), expected_statuses.count())

        for status in expected_statuses:
            self.assertContains(response, status.name)

    def test_create_status(self):
        form_data = {
            'name': 'Close',
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))

        self.assertTrue(Status.objects.filter(name='Close').exists())

    def test_update_status(self):
        form_data = {
            'name': 'Updated',
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('statuses:update', args=[self.status.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))

        self.status.refresh_from_db()

        self.assertEqual(self.status.name, form_data['name'])

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:delete', args=[self.status.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses:index'))

        status_exists = Status.objects.filter(pk=self.status.pk).exists()
        self.assertFalse(status_exists)

    def test_anonymous_index_status(self):
        response = self.client.get(reverse('statuses:index'))

        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('statuses:index')
        self.assertRedirects(response, expected_url)

    def test_anonymous_create_status(self):
        form_data = {
            'name': 'Close',
        }

        response = self.client.post(reverse('statuses:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('statuses:create')
        self.assertRedirects(response, expected_url)

        self.assertFalse(Status.objects.filter(name='Close').exists())

    def test_anonymous_update_status(self):
        form_data = {
            'name': 'Updated',
        }

        original_status_name = self.status.name

        response = self.client.post(
            reverse('statuses:update', args=[self.status.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)

        expected_url = (
            reverse('login')
            + '?next='
            + reverse('statuses:update', args=[self.status.pk])
        )
        self.assertRedirects(response, expected_url)

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, original_status_name)

    def test_anonymous_delete_status(self):
        response = self.client.post(reverse('statuses:delete', args=[self.status.pk]))

        self.assertEqual(response.status_code, 302)

        expected_url = (
            reverse('login')
            + '?next='
            + reverse('statuses:delete', args=[self.status.pk])
        )
        self.assertRedirects(response, expected_url)

        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
