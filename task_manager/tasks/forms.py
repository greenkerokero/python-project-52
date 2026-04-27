from django.forms import ModelForm

from task_manager.tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee']

    def __init__(self, *args, **kwargs):
        # 1. Сначала вызываем стандартную инициализацию формы
        super().__init__(*args, **kwargs)

        # 2. Подменяем функцию генерации имени (label) для поля assignee
        # Теперь форма будет вызывать get_full_name() у каждого юзера
        self.fields['assignee'].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )
