from django.contrib.auth import get_user_model
from task_manager.labels.models import Label
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class LabelTest(TestCase):
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        translation.activate('en')
        self.user = get_user_model().objects.get(pk=10001)
        self.password = 'Strongpass1!'
        self.user.set_password(self.password)
        self.user.save()
        self.label = Label.objects.get(pk=40001)

    def test_label_index(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('labels:index'))
        expected_labels = Label.objects.all()

        labels_in_context = response.context['label_list']
        self.assertEqual(len(labels_in_context), expected_labels.count())

        for label in expected_labels:
            self.assertContains(response, label.name)

    def test_create_label(self):
        form_data = {
            "name": "New Label",
        }

        self.client.force_login(self.user)

        response = self.client.post(reverse('labels:create'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))

        self.assertTrue(
            Label.objects.filter(name=form_data['name']).exists()
        )

    def test_update_label(self):
        form_data = {
            "name": "New Label",
        }

        self.client.force_login(self.user)
        response = self.client.post(
            reverse('labels:update', args=[self.label.pk]), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))

        self.label.refresh_from_db()

        self.assertEqual(self.label.name, form_data['name'])

    def test_delete_label(self):
        label_to_delete = Label.objects.get(pk=40003)

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:delete', args=[label_to_delete.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))

        label_exists = Label.objects.filter(pk=label_to_delete.pk).exists()
        self.assertFalse(label_exists)

    def test_anonymous_index_label(self):
        response = self.client.get(reverse('labels:index'))

        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('labels:index')
        self.assertRedirects(response, expected_url)

    def test_anonymous_create_label(self):
        form_data = {
            "name": "Hacked Label",
        }
        response = self.client.post(reverse('labels:create'), data=form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('labels:create')
        self.assertRedirects(response, expected_url)
        self.assertFalse(Label.objects.filter(name=form_data['name']).exists())

    def test_anonymous_update_label(self):
        form_data = {
            "name": "Hacked Label",
        }
        response = self.client.post(
            reverse('labels:update', args=[self.label.pk]), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('labels:update', args=[self.label.pk])
        self.assertRedirects(response, expected_url)
        self.label.refresh_from_db()
        self.assertNotEqual(self.label.name, form_data['name'])

    def test_anonymous_delete_label(self):
        response = self.client.post(reverse('labels:delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        expected_url = reverse('login') + '?next=' + reverse('labels:delete', args=[self.label.pk])
        self.assertRedirects(response, expected_url)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_delete_label_with_tasks(self):
        from task_manager.tasks.models import Task
        task = Task.objects.first()
        task.labels.add(self.label)

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:delete', args=[self.label.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels:index'))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
