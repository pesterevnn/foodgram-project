# Generated by Django 3.2.3 on 2021-06-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_recipes_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
