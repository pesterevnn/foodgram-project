from django.forms import ModelForm, Textarea, ValidationError

from .models import Recipe


class RecipeCreateForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'cooking_time', 'description', 'image']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form__input'
        self.fields['tags'].widget.attrs['class'] = 'form__input'
        self.fields['cooking_time'].widget.attrs['class'] = 'form__input'
        self.fields['description'].widget.attrs['class'] = 'form__textarea'
        self.fields['image'].widget.attrs['class'] = 'file'

    def clean(self):
        data = self.cleaned_data
        for key in data.keys():
            if key[:14] == 'nameIngredient':
                index = key[-1]
                value_ing = data[f'valueIngredient_{index}']
                if value_ing < 0:
                    raise ValidationError("Количество ингредиентов не может быть меньше нуля!")
        return data
