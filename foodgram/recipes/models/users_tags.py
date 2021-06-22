from django.conf import settings
from django.db import models

from .tags import Tags


class UsersTags(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='userstags',
    )
    tag = models.ForeignKey(
        Tags,
        verbose_name='Тэг',
        on_delete=models.CASCADE,
        related_name='userstags',
        help_text='Добавленный в избранное рецепт'
    )
    active = models.BooleanField(
        verbose_name='Active',
        default=True,
    )

    class Meta:
        verbose_name = 'Пользовательский Тэг'
        verbose_name_plural = 'Пользовательские тэги'
        ordering = ['pk']
