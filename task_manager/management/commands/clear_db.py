from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class Command(BaseCommand):
    help = 'Clears the database (keeps superusers)'

    def handle(self, *args, **options):
        Task.objects.all().delete()
        self.stdout.write('Tasks deleted')

        Status.objects.all().delete()
        Label.objects.all().delete()
        self.stdout.write('Statuses and Labels deleted')

        user = get_user_model()
        user.objects.filter(is_superuser=False).delete()
        self.stdout.write('Users deleted (keeps superusers)')

        self.stdout.write('Database successfully cleared')
