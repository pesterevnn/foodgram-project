from django.db import models

from .ingredients import Ingredients
from .recipes import Recipes


class Ingredients_Recipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ['ingredient']

    def __str__(self):
        return f'{self.ingredient.title} - \
                 {self.amount} {self.ingredient.dimension}'
