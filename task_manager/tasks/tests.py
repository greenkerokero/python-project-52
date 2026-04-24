from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


class TaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        translation.activate('en')
        self.user = get_user_model().objects.get(pk=10001)
        self.password = 'Strongpass1!'
        self.user.set_password(self.password)
        self.user.save()
        self.status = Status.objects.get(pk=20001)
        self.task = Task.objects.get(pk=30001)

    def test_task_index(self):
        response = self.client.get(reverse('tasks:index'))
        expected_tasks = Task.objects.all()

        tasks_in_context = response.context['task_list']
        self.assertEqual(len(tasks_in_context), expected_tasks.count())

        for task in expected_tasks:
            self.assertContains(response, task.name)

    def test_create_task(self):
        form_data = {
            'name': 'test task',
            'reporter': [self.user],
            'status': [self.status],
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))

        self.assertTrue(Task.objects.filter(name=form_data['name']).exists())

    def test_update_task(self):
        form_data = {
            'name': 'update task',
            'reporter': [self.user],
            'status': [self.status],
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('tasks:update', args=[self.task.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))

        self.status.refresh_from_db()

        self.assertEqual(self.task.name, form_data['name'])

    def test_delete_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks:index'))

        task_exists = Task.objects.filter(pk=self.task.pk).exists()
        self.assertFalse(task_exists)

    def test_anonymous_create_task(self):
        form_data = {
            'name': 'test task',
            'reporter': [self.user],
            'status': [self.status],
        }

        response = self.client.post(reverse('tasks:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('tasks:create')
        self.assertRedirects(response, expected_url)

        self.assertFalse(Task.objects.filter(name=form_data['name']).exists())

    def test_anonymous_delete_task(self):
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))

        self.assertEqual(response.status_code, 302)

        expected_url = (
                reverse('login')
                + '?next='
                + reverse('tasks:delete', args=[self.task.pk])
        )
        self.assertRedirects(response, expected_url)

        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_another_user_delete_status(self):
        self.client.force_login(self.user)
        another_user = get_user_model().objects.get(pk=10002)
        response = self.client.post(reverse('tasks:delete', args=[another_user.pk]))

        self.assertEqual(response.status_code, 302)

        expected_url = (
                reverse('login')
                + '?next='
                + reverse('tasks:delete', args=[self.task.pk])
        )
        self.assertRedirects(response, expected_url)

        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
