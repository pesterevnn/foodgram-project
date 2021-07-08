from django.db import models


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name='Наименование',
        max_length=150,
        db_index=True,
        help_text='Укажите наименование ингридиента',
    )
    dimension = models.CharField(
        verbose_name='Ед. изм.',
        max_length=20,
        help_text='Укажите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'
