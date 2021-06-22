from .favoriterecipes import FavoriteRecipes
from .follows import Follows
from .ingredients import Ingredients
from .ingredients_recipe import Ingredients_Recipe
from .purchases import Purchases
from .recipes import Recipes
from .tags import Tags
from .users_tags import UsersTags

__all__ = [
    Recipes,
    Ingredients,
    Ingredients_Recipe,
    Follows,
    FavoriteRecipes,
    Purchases,
    Tags,
    UsersTags,
]
