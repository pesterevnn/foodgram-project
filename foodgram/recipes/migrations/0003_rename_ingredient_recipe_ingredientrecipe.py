# Generated by Django 3.2.3 on 2021-06-28 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredient_Recipe',
            new_name='IngredientRecipe',
        ),
    ]