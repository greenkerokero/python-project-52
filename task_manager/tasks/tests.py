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
