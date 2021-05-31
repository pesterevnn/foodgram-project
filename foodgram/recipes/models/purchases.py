from django.db import models
from django.conf import settings

from .recipes import Recipes


class Purchases(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
        related_name='customer',
        help_text='Тот кто включает в список покупок',
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='purchases',
        help_text='Добавленный в избранное рецепт'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'recipe'],
                name='unique_purchase'
            ),
        ]
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['customer']
