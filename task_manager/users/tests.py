from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import translation


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        translation.activate('en')
        self.user = get_user_model().objects.get(pk=10001)
        self.password = 'Strongpass1!'
        self.user.set_password(self.password)
        self.user.save()

    def test_index(self):
        response = self.client.get(reverse('users:index'))
        expected_users = get_user_model().objects.exclude(is_superuser=True)

        users_in_context = response.context['user_list']
        self.assertEqual(len(users_in_context), expected_users.count())

        for user in expected_users:
            self.assertContains(response, user.username)
