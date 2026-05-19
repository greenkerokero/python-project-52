from django.contrib import admin

from task_manager.tasks.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'reporter',
        'assignee',
        'created_at',
    )
    search_fields = ('name', 'description')
    list_filter = ('status', 'reporter', 'assignee', 'labels')
    list_display_links = ('id', 'name')
