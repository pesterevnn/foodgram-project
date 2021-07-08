import json
from recipes.models import Ingredient


if __name__ == '__main__':

    with open('ingredients.json') as json_data:
        data = json.load(json_data,)

    for item in data:
        new_ingredient = Ingredient(title=item['title'], dimension=item['dimension'])
        new_ingredient.save()
        break
