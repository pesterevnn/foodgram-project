from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Recipes, Purchases, Follows, Ingredients_Recipe
from .models import FavoriteRecipes, Tags
from .forms import RecipeCreateForm

def index(request):
    curent_user = request.user
    recipes = Recipes.objects.all()
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

def tag_filter(request, tag_id, action):
    curent_user = request.user
    tag = Tags
    recipes = Recipes.objects.all()
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        purchases_count = purchases.count()
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases_count = 0
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'index.html', context)

def favorite(request):
    curent_user = request.user
    recipes = Recipes.objects.filter(favorite_authors__user=curent_user)
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
    user = get_object_or_404(get_user_model(), username=username)
    recipes = Recipes.objects.filter(author=user)
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
        favorite_recipes = FavoriteRecipes.objects.filter(user=curent_user)
        fav_recipes_count = favorite_recipes.count()
    else:
        favorite_recipes = None
        fav_recipes_count = 0
        purchases_count = 0
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'author': user,
        'purchases_count': purchases_count,
        'section': section,
        'fav_recipes_count': fav_recipes_count,
        'favorite_recipes': favorite_recipes,
    }
    return render(request, 'authorRecipe.html', context)    

def follow(request):
    curent_user = request.user
    follows = Follows.objects.filter(subscriber=curent_user)
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
    else:
        purchases_count = 0
        is_favorite = False
    context = {
        'user': curent_user,
        'purchases_count': purchases_count,
        'section': section,
        'recipe': recipe,
        'ingredients': ingredients,
        'is_favorite': is_favorite,
    }
    return render(request, 'singlePage.html', context)

#def create_recipe(request):
#    curent_user = request.user
#    section = request.resolver_match.url_name
#    if curent_user.is_authenticated:
#        purchases = Purchases.objects.filter(customer = curent_user)
#        purchases_count = purchases.count()
#    else:
#        purchases_count = 0
#    form = RecipeCreateForm(request.POST or None, files=request.FILES or None)
#    if form.is_valid():
#        recipe = form.save(commit=False)
#        recipe.author = curent_user
#        recipe.save()
#        return redirect('index')
#    context = {
#        'user': curent_user,
#        'section': section,
#        'purchases_count': purchases_count,
#        'form': form, 
#        'added': True,
#    }
#   return render(request, 'formRecipe.html', context)

# как вариант попробовать
class RecipeCreate(CreateView):
    form_class = RecipeCreateForm
    success_url = reverse_lazy("index")
    template_name = "formRecipe.html"


@login_required
def profile_follow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    user = request.user
    if not author == user:
        Follows.objects.get_or_create(subscriber=user, author=author)
    return redirect('follow')


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    user = request.user
    follow = get_object_or_404(Follows, subscriber=user, author=author)
    follow.delete()
    return redirect('follow')

@login_required
def del_purchase(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    purchase = get_object_or_404(Purchases, customer=user, recipe=recipe)
    purchase.delete()
    return redirect('shoplist')

@login_required
def add_purchase(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    Purchases.objects.get_or_create(customer=user, recipe=recipe)
    return redirect('shoplist')

@login_required
def add_favorite(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    FavoriteRecipes.objects.get_or_create(user=user, recipe=recipe)
    return redirect('favorite')

@login_required
def del_favorite(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    favorite_recipe = get_object_or_404(FavoriteRecipes, user=user, recipe=recipe)
    favorite_recipe.delete()
    return redirect('favorite')
