from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        translation.activate('en')
        self.user = get_user_model().objects.get(pk=10001)
        self.password = 'Strongpass1!'
        self.user.set_password(self.password)
        self.user.save()

    def test_user_index(self):
        response = self.client.get(reverse('users:index'))
        expected_users = get_user_model().objects.exclude(is_superuser=True)

        users_in_context = response.context['user_list']
        self.assertEqual(len(users_in_context), expected_users.count())

        for user in expected_users:
            self.assertContains(response, user.username)

    def test_create_user(self):
        form_data = {
            'username': 'create_testing_user',
            'first_name': 'Create',
            'last_name': 'UserC',
            'password1': 'CreateSafePassword123!',
            'password2': 'CreateSafePassword123!',
        }

        response = self.client.post(reverse('users:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        self.assertTrue(
            get_user_model()
            .objects.filter(username='create_testing_user')
            .exists()
        )

    def test_update_user(self):
        form_data = {
            'first_name': 'Update',
            'last_name': 'UserU',
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:update', args=[self.user.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, form_data['first_name'])
        self.assertEqual(self.user.last_name, form_data['last_name'])

    def test_delete_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users:delete', args=[self.user.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:index'))

        user_exists = get_user_model().objects.filter(pk=self.user.pk).exists()
        self.assertFalse(user_exists)

    def test_anonymous_update_user(self):
        form_data = {
            'first_name': 'Update',
            'last_name': 'UserU',
        }

        original_first_name = self.user.first_name
        original_last_name = self.user.last_name

        response = self.client.post(
            reverse('users:update', args=[self.user.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)

        expected_url = (
            reverse('login')
            + '?next='
            + reverse('users:update', args=[self.user.pk])
        )
        self.assertRedirects(response, expected_url)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, original_first_name)
        self.assertEqual(self.user.last_name, original_last_name)

    def test_anonymous_delete_user(self):
        response = self.client.post(
            reverse('users:delete', args=[self.user.pk])
        )

        self.assertEqual(response.status_code, 302)

        expected_url = (
            reverse('login')
            + '?next='
            + reverse('users:delete', args=[self.user.pk])
        )
        self.assertRedirects(response, expected_url)

        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )

    def test_another_user_update(self):
        form_data = {
            'first_name': 'Update',
            'last_name': 'UserU',
        }

        self.client.force_login(self.user)
        target_user = get_user_model().objects.get(pk=10002)

        original_first_name = target_user.first_name
        original_last_name = target_user.last_name

        response = self.client.post(
            reverse('users:update', args=[target_user.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)

        expected_url = reverse('users:index')
        self.assertRedirects(response, expected_url)

        target_user.refresh_from_db()
        self.assertEqual(target_user.first_name, original_first_name)
        self.assertEqual(target_user.last_name, original_last_name)

    def test_another_user_delete(self):
        self.client.force_login(self.user)
        target_user = get_user_model().objects.get(pk=10002)

        response = self.client.post(
            reverse('users:delete', args=[target_user.pk])
        )

        self.assertEqual(response.status_code, 302)

        expected_url = reverse('users:index')
        self.assertRedirects(response, expected_url)

        self.assertTrue(
            get_user_model().objects.filter(pk=target_user.pk).exists()
        )
