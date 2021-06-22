from django.db import models


class Tags(models.Model):
    VALUES_TAGS = [
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner')
    ]
    tag = models.CharField(
        verbose_name='Таг',
        max_length=10,
        choices=VALUES_TAGS
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=50,
        blank=True,
    )
    color = models.CharField(
        verbose_name='Color',
        max_length=50,
        blank=True
    )
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['pk']
        constraints = [
            models.UniqueConstraint(
                fields=['tag',],
                name='unique_tag'
            ),
        ]
    def __str__(self) -> str:
        return self.tag
