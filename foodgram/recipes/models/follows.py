from django.conf import settings
from django.db import models


class Follows(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber',
        help_text='Тот кто подписывается',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
        help_text='Тот на кого подписываются',
    )

    def get_first_three_recipes(self):
        recipes = self.author.recipes.all()[:3]
        return recipes

    def count_without_3(self):
        count = self.author.recipes.count()
        count_without_3 = count - 3
        return count_without_3

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_follow'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['subscriber']
