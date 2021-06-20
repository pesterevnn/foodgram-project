from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Recipes, Purchases, Follows, Ingredients_Recipe
from .models import FavoriteRecipes, Tags, Ingredients
from .forms import RecipeCreateForm

def index(request):
    curent_user = request.user
    recipes = Recipes.objects.all()
    tags = Tags.objects.all()
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        purchases_count = purchases.count()
        ids_recipes_list_in_purchases = get_ids_recipes_list_in_purchases(purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_list_in_favorite(favorite_recipes)
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases = None
        purchases_count = 0
        ids_recipes_list_in_purchases = []
        ids_recipes_list_in_favorite = []
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'tags': tags,
        'recipes': recipes,
        'ids_recipes_list_in_purchases': ids_recipes_list_in_purchases,
        'ids_recipes_list_in_favorite': ids_recipes_list_in_favorite,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'index.html', context)

def get_ids_recipes_list_in_purchases(purchases):
    ids_list = []
    for item in purchases:
        ids_list.append(item.recipe.pk)
    return ids_list

def get_ids_recipes_list_in_favorite(favorite_recipes):
    ids_list = []
    for item in favorite_recipes:
        ids_list.append(item.recipe.pk)
    return ids_list

def get_ids_authors_in_follows(follows):
    ids_list = []
    for item in follows:
        ids_list.append(item.author.pk)
    return ids_list

def favorite(request):
    curent_user = request.user
    recipes = Recipes.objects.filter(favorite_authors__user=curent_user)
    tags = Tags.objects.all()
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        ids_recipes_list_in_purchases = get_ids_recipes_list_in_purchases(purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_list_in_favorite(favorite_recipes)
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases_count = 0
        ids_recipes_list_in_purchases = []
        ids_recipes_list_in_favorite = []
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'tags': tags,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
        'ids_recipes_list_in_purchases': ids_recipes_list_in_purchases,
        'ids_recipes_list_in_favorite': ids_recipes_list_in_favorite,
    }
    return render(request, 'favorite.html', context)

def profile(request, username):
    curent_user = request.user
    tags =  Tags.objects.all()
    user = get_object_or_404(get_user_model(), username=username)
    recipes = Recipes.objects.filter(author=user)
    is_follow = Follows.objects.filter(subscriber=curent_user, author=user).exists()
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        ids_recipes_list_in_purchases = get_ids_recipes_list_in_purchases(purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_list_in_favorite(favorite_recipes)
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases_count = 0
        ids_recipes_list_in_purchases = []
        ids_recipes_list_in_favorite = []
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'tags': tags,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'author': user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
        'ids_recipes_list_in_purchases': ids_recipes_list_in_purchases,
        'ids_recipes_list_in_favorite': ids_recipes_list_in_favorite,
        'is_follow': is_follow,
    }
    return render(request, 'authorRecipe.html', context)    

def follow(request):
    curent_user = request.user
    follows = Follows.objects.filter(subscriber=curent_user)
    ids_follows_author = get_ids_authors_in_follows(follows)
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
        purchases_count = 0
    paginator = Paginator(follows, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'paginator': paginator,
        'user': curent_user,
        'follows': follows,
        'purchases_count': purchases_count,
        'section': section,
        'ids_follows_author': ids_follows_author,
    }
    return render(request, 'myFollow.html', context)

def shoplist(request):
    curent_user = request.user
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
        purchases = None
        purchases_count = 0
    section = request.resolver_match.url_name
    context = {
        'user': curent_user,
        'purchases_count': purchases_count,
        'purchases': purchases,
        'section': section,
    }
    return render(request, 'shopList.html', context)

def recipe(request, recipe_id):
    curent_user = request.user
    recipe = Recipes.objects.get(pk=recipe_id)
    ingredients = Ingredients_Recipe.objects.filter(recipe=recipe)
    section = request.resolver_match.url_name
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
        is_favorite = FavoriteRecipes.objects.filter(user=curent_user, recipe=recipe).exists()
        is_in_purcheses = Purchases.objects.filter(customer=curent_user, recipe=recipe).exists()
        is_in_follow = Follows.objects.filter(subscriber=curent_user, author=recipe.author)
    else:
        purchases_count = 0
        is_favorite = False
        is_in_purcheses = False
        is_in_follow = False
    context = {
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'recipe': recipe,
        'ingredients': ingredients,
        'is_favorite': is_favorite,
        'is_in_purcheses': is_in_purcheses,
        'is_in_follow': is_in_follow,
    }
    return render(request, 'singlePage.html', context)

def create_recipe(request):
    curent_user = request.user
    tags = Tags.objects.all()
    section = request.resolver_match.url_name
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
        purchases_count = 0
    form = RecipeCreateForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = curent_user
        recipe.save()
        recipe.tags.set(get_tags_ids(request.POST))
        ing_for_recipes = get_ingredients_for_recipe(request.POST)
        if ing_for_recipes:
            ids_ifr = []
            for key in ing_for_recipes.keys():
                ingredient = Ingredients.objects.get(pk=key)
                amount = ing_for_recipes[key]
                ing_recipe = Ingredients_Recipe(recipe=recipe, ingredient=ingredient, amount=amount)
                ing_recipe.save()
                ids_ifr.append(ing_recipe.id)
        recipe.save()
        return redirect('index')
    context = {
        'user': curent_user,
        'section': section,
        'purchases_count': purchases_count,
        'author': curent_user,
        'form': form,
        'tags': tags,
        'added': True,
    }
    return render(request, 'formRecipe.html', context)

def get_tags_ids(post_dict):
    tags_ids = []
    if post_dict.get('breakfast'):
        tags_ids.append(Tags.objects.get(tag='breakfast').id)
    if post_dict.get('lunch'):
        tags_ids.append(Tags.objects.get(tag='lunch').id)
    if post_dict.get('dinner'):
        tags_ids.append(Tags.objects.get(tag='dinner').id)
    return tags_ids

def get_ingredients_for_recipe(post_dict):
    ingredients_recipe_dic = {}
    for key in post_dict.keys():
        if key[:14] == 'nameIngredient':
            index = key[-1]
            name_ing = post_dict[key]
            value_ing = post_dict[f"valueIngredient_{index}"]
            units_ing = post_dict[f"unitsIngredient_{index}"]
            ing_id = Ingredients.objects.get(title=name_ing, dimension=units_ing).id
            ingredients_recipe_dic[ing_id] = value_ing 
    return ingredients_recipe_dic

def change_recipe(request, recipe_id):
    tags = Tags.objects.all()
    recipe = get_object_or_404(
        Recipes,
        id=recipe_id
    )

    ingredients_recipe = []
    for ingredient in recipe.ingredients.all():
        ingr_recipe = Ingredients_Recipe.objects.get(recipe=recipe, ingredient=ingredient)
        ingredients_recipe.append(ingr_recipe)

    curent_user = request.user
    section = request.resolver_match.url_name
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
        purchases_count = 0
    form = RecipeCreateForm(
        request.POST or None,
        files=request.FILES or None, 
        instance=recipe
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = curent_user
        recipe.tags.set(get_tags_ids(request.POST))
        ing_for_recipes = get_ingredients_for_recipe(request.POST)
        if ing_for_recipes:
            ids_ifr = []
            for key in ing_for_recipes.keys():
                ingredient = Ingredients.objects.get(pk=key)
                amount = ing_for_recipes[key]
                ing_recipe = Ingredients_Recipe(recipe=recipe, ingredient=ingredient, amount=amount)
                ing_recipe.save()
                ids_ifr.append(ing_recipe.id)
        recipe.save()
        return redirect(
                'recipe',
                recipe_id=recipe.pk
        )
    context = {
        'user': curent_user,
        'recipe': recipe,
        'section': section,
        'purchases_count': purchases_count,
        'form': form,
        'tags': tags,
        'ingredients_recipe': ingredients_recipe,
        'added': False,
    }
    return render(request, 'formRecipe.html', context)


@login_required
def delete_recipe(request, recipe_id):
    recipe = Recipes.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect('index')


def tag_filter(request):
    curent_user = request.user

    recipes = Recipes.objects.all()
    tags = Tags.objects.all()
    
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        purchases_count = purchases.count()
        ids_recipes_list_in_purchases = get_ids_recipes_list_in_purchases(purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_list_in_favorite(favorite_recipes)
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases = None
        purchases_count = 0
        ids_recipes_list_in_purchases = []
        ids_recipes_list_in_favorite = []
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'tags': tags,
        'recipes': recipes,
        'ids_recipes_list_in_purchases': ids_recipes_list_in_purchases,
        'ids_recipes_list_in_favorite': ids_recipes_list_in_favorite,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
    }
    return redirect(request, 'index.html', context)