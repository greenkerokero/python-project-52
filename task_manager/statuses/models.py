from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name'),
        error_messages={
            'unique': _('Status with this Name already exists.')
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')

    def __str__(self):
        return self.name
