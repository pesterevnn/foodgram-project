from django.forms import ModelForm

from .models import Recipes


class RecipeForm(ModelForm):
    class Meta:
        model = Recipes
        fields = ['title', 'tags', 'ingredients', 'cooking_time', 'description', 'image']
