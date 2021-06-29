import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import RecipeCreateForm
from .models import (FavoriteRecipe, Follow, Ingredient, IngredientRecipe,
                     Purchase, Recipe)
from .utils import (get_all_ingredients_from_shoplist,
                    get_filtered_recipes_by_tags, get_ids_authors_in_follows,
                    get_ids_recipes_in_favorite, get_ingredients_for_recipe,
                    get_tags_ids)


def index(request):
    curent_user = request.user
    if curent_user.is_authenticated:
        recipes = get_filtered_recipes_by_tags(request)
    else:
        recipes = Recipe.objects.all()
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
    }
    return render(request, 'index.html', context)


def favorite(request):
    curent_user = request.user
    if curent_user.is_authenticated:
        favorite_recipes = FavoriteRecipe.objects.filter(
            user=curent_user)
        ids_recipes_list_in_favorite = get_ids_recipes_in_favorite(
            favorite_recipes)
        recipes = get_filtered_recipes_by_tags(
            request,
            ids_recipes_list_in_favorite
        )
    else:
        recipes = get_filtered_recipes_by_tags(request)
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
    }
    return render(request, 'favorite.html', context)


def profile(request, username):
    curent_user = request.user
    user = get_object_or_404(get_user_model(), username=username)
    if request.user.is_authenticated:
        recipes = get_filtered_recipes_by_tags(request, None, user)
        is_follow = Follow.objects.filter(
            subscriber=curent_user,
            author=user).exists()
    else:
        recipes = Recipe.objects.filter(author=user)
        is_follow = False
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
        'author': user,
        'is_follow': is_follow,
    }
    return render(request, 'authorRecipe.html', context)


def follow(request):
    curent_user = request.user
    follows = Follow.objects.filter(subscriber=curent_user)
    ids_follows_author = get_ids_authors_in_follows(follows)
    paginator = Paginator(follows, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'follows': follows,
        'ids_follows_author': ids_follows_author,
    }
    return render(request, 'myFollow.html', context)


def shoplist(request):
    return render(request, 'shopList.html',)


def recipe(request, recipe_id):
    curent_user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = IngredientRecipe.objects.filter(recipe=recipe)
    if curent_user.is_authenticated:
        is_favorite = FavoriteRecipe.objects.filter(
            user=curent_user,
            recipe=recipe).exists()
        is_in_purcheses = Purchase.objects.filter(
            customer=curent_user,
            recipe=recipe).exists()
        is_in_follow = Follow.objects.filter(
            subscriber=curent_user,
            author=recipe.author
        )
    else:
        is_favorite = False
        is_in_purcheses = False
        is_in_follow = False
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'is_favorite': is_favorite,
        'is_in_purcheses': is_in_purcheses,
        'is_in_follow': is_in_follow,
    }
    return render(request, 'singlePage.html', context)


def create_or_edit_recipe(request, recipe_id=None):
    curent_user = request.user
    ingredients_recipe = []
    if recipe_id is not None:
        added = False
        recipe = get_object_or_404(
            Recipe,
            id=recipe_id
        )
        for ingredient in recipe.ingredients.all():
            ingr_recipe = get_object_or_404(
                IngredientRecipe,
                recipe=recipe,
                ingredient=ingredient
            )
            ingredients_recipe.append(ingr_recipe)
        form = RecipeCreateForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
    else:
        recipe = None
        added = True
        form = RecipeCreateForm(
            request.POST or None,
            files=request.FILES or None
        )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = curent_user
        recipe.save()
        recipe.tags.set(get_tags_ids(request.POST))
        ing_for_recipes = get_ingredients_for_recipe(request.POST)
        if ing_for_recipes:
            ids_ifr = []
            for key in ing_for_recipes.keys():
                ingredient = get_object_or_404(Ingredient, pk=key)
                amount = ing_for_recipes[key]
                ing_recipe = IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
                ing_recipe.save()
                ids_ifr.append(ing_recipe.id)
        recipe.save()
        if recipe_id is None:
            return redirect('index')
        else:
            return redirect(
                'recipe',
                recipe_id=recipe.pk
            )
    context = {
        'recipe': recipe,
        'author': curent_user,
        'form': form,
        'ingredients_recipe': ingredients_recipe,
        'added': added,
    }
    return render(request, 'formRecipe.html', context)


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('index')


pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))


def download_shoplist(request):
    total_ingredients_dict = get_all_ingredients_from_shoplist(
        request)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Vera', 14)
    p.drawString(250, 800, 'My SHOPLIST')
    h = 760
    for ingredient in total_ingredients_dict.keys():
        p.drawString(
            100,
            h,
            f"- {ingredient.title} ({ingredient.dimension}) \
                - {total_ingredients_dict[ingredient]}")
        h = h - 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='shoplist.pdf'
    )


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
