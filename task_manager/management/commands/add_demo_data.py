from random import choice, randint, sample

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class Command(BaseCommand):
    help = 'Populates the database with fake English data'

    def handle(self, *args, **options):
        fake = Faker('en_US')
        user = get_user_model()

        users = []
        self.stdout.write('--------------- Generated demo users ---------------')

        for _ in range(5):
            username = fake.unique.user_name()
            password = fake.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )

            user, created = user.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.unique.email(),
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'Login: {username:20} | Password: {password}')
            users.append(user)

        status_names = ['New', 'In Progress', 'In Review', 'Done', 'Archived']
        statuses = []
        for name in status_names:
            status, _ = Status.objects.get_or_create(name=name)
            statuses.append(status)

        label_names = ['Bug', 'Enhancement', 'Urgent', 'Documentation', 'Refactoring']
        labels = []
        for name in label_names:
            label, _ = Label.objects.get_or_create(name=name)
            labels.append(label)

        for _ in range(5):
            task, created = Task.objects.get_or_create(
                name=fake.sentence(nb_words=4).replace('.', ''),
                defaults={
                    'description': fake.text(max_nb_chars=200),
                    'status': choice(statuses),
                    'reporter': choice(users),
                    'assignee': choice(users),
                },
            )
            if created:
                random_labels = sample(labels, k=randint(1, 3))
                task.labels.set(random_labels)
