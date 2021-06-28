from ..models import FavoriteRecipes, Purchases
from ..utils import get_ids_recipes_in_favorite, get_ids_recipes_in_purchases


def get_favorite_recipes(request):
    curent_user = request.user
    if request.user.is_authenticated:
        favorite_recipes = FavoriteRecipes.objects.filter(
            user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        purchases = Purchases.objects.filter(customer=curent_user)
        ids_recipes_list_in_purchases = get_ids_recipes_in_purchases(
            purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_in_favorite(
            favorite_recipes)
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        ids_recipes_list_in_purchases = []
        ids_recipes_list_in_favorite = []
    return {
        'favorite_recipes': favorite_recipes,
        'fav_recipes_count': fav_recipes_count,
        'ids_recipes_list_in_purchases': ids_recipes_list_in_purchases,
        'ids_recipes_list_in_favorite': ids_recipes_list_in_favorite,
    }
