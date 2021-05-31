from django.db import models


class Tags(models.Model):
    VALUES_TAGS = [
        ('B', 'breakfast'),
        ('L', 'lunch'),
        ('D', 'dinner')
    ]
    tag = models.CharField(
        verbose_name='Таг',
        max_length=1,
        choices=VALUES_TAGS
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=50,
        blank=True,
    )
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        constraints = [
            models.UniqueConstraint(
                fields=['tag',],
                name='unique_tag'
            ),
        ]
    def __str__(self) -> str:
        return self.tag