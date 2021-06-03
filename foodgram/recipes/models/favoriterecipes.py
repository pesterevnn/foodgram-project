from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404

from ..models import Recipes


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        help_text='Тот кто включает в избранное',
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_authors',
        help_text='Добавленный в избранное рецепт'
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            ),
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['user']
