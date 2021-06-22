from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from reportlab.pdfgen import canvas

from .forms import RecipeCreateForm
from .models import (FavoriteRecipes, Follows, Ingredients,
                     Ingredients_Recipe, Purchases, Recipes, Tags,
                     UsersTags)


def get_usertags(request):
    user = request.user
    users_tags = user.userstags.all()
    return users_tags


def set_active_userstags(request):
    user = request.user
    tags = Tags.objects.all()
    users_tags = []
    if user.is_authenticated:
        for tag in tags:
            values_for_update = {
                "user": user,
                "tag": tag,
                'active': True
            }
            users_tag, created = UsersTags.objects.update_or_create(
                user=user,
                tag=tag,
                defaults=values_for_update
            )
            users_tags.append(users_tag)
    return users_tags


def get_actual_userstags(request, tag_click):
    curent_user = request.user
    users_tags = []
    if tag_click is not None:
        tag_id = Tags.objects.get(tag=tag_click).id
        tag = UsersTags.objects.get(tag=tag_id, user=curent_user)
        tag_swch = request.GET.get('swch')
        if tag_swch == 'off':
            tag.active = False
        else:
            tag.active = True
        tag.save()
        users_tags = curent_user.userstags.all()
    elif request.GET.get('page') is None:
        users_tags = set_active_userstags(request)
    else:
        users_tags = get_usertags(request)
    return users_tags


def get_filtertags_active(request):
    tag_click = request.GET.get('tag')
    users_tags = get_actual_userstags(request, tag_click)
    filtered_tags_id = []
    for item in users_tags:
        if item.active:
            filtered_tags_id.append(item.tag.id)
    return filtered_tags_id


def index(request):

    tags = Tags.objects.all()
    curent_user = request.user

    tag_click = request.GET.get('tag')
    users_tags = get_actual_userstags(request, tag_click)
    filtered_tags_id = []
    for item in users_tags:
        if item.active:
            filtered_tags_id.append(item.tag.id)
    recipes = Recipes.objects.filter(
        tags__in=filtered_tags_id).distinct()

    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        favorite_recipes = FavoriteRecipes.objects.filter(
            user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        purchases_count = purchases.count()
        ids_recipes_list_in_purchases = get_ids_recipes_in_purchases(
            purchases
        )
        ids_recipes_list_in_favorite = get_ids_recipes_in_favorite(
            favorite_recipes
        )
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
        'users_tags': users_tags,
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


def get_ids_recipes_in_purchases(purchases):
    ids_list = []
    for item in purchases:
        ids_list.append(item.recipe.pk)
    return ids_list


def get_ids_recipes_in_favorite(favorite_recipes):
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
    tags = Tags.objects.all()
    curent_user = request.user

    tag_click = request.GET.get('tag')
    users_tags = get_actual_userstags(request, tag_click)
    filtered_tags_id = []
    for item in users_tags:
        if item.active:
            filtered_tags_id.append(item.tag.id)
    recipes = Recipes.objects.filter(
        tags__in=filtered_tags_id).distinct()

    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        purchases_count = purchases.count()
        favorite_recipes = FavoriteRecipes.objects.filter(
            user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        ids_recipes_list_in_purchases = get_ids_recipes_in_purchases(
            purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_in_favorite(
            favorite_recipes)
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
        'users_tags': users_tags,
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
    tags = Tags.objects.all()

    user = get_object_or_404(get_user_model(), username=username)

    tag_click = request.GET.get('tag')
    users_tags = get_actual_userstags(request, tag_click)
    filtered_tags_id = []
    for item in users_tags:
        if item.active:
            filtered_tags_id.append(item.tag.id)

    recipes = Recipes.objects.filter(
        author=user,
        tags__in=filtered_tags_id).distinct()

    if request.user.is_authenticated:
        is_follow = Follows.objects.filter(
            subscriber=curent_user,
            author=user).exists()
        purchases = Purchases.objects.filter(customer=curent_user)
        purchases_count = purchases.count()
        favorite_recipes = FavoriteRecipes.objects.filter(
            user=curent_user)
        fav_recipes_count = favorite_recipes.count()
        ids_recipes_list_in_purchases = get_ids_recipes_in_purchases(
            purchases)
        ids_recipes_list_in_favorite = get_ids_recipes_in_favorite(
            favorite_recipes)
    else:
        is_follow = False
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
        'users_tags': users_tags,
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
        purchases = Purchases.objects.filter(customer=curent_user)
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
        purchases = Purchases.objects.filter(customer=curent_user)
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
        purchases = Purchases.objects.filter(customer=curent_user)
        purchases_count = purchases.count()
        is_favorite = FavoriteRecipes.objects.filter(
            user=curent_user,
            recipe=recipe).exists()
        is_in_purcheses = Purchases.objects.filter(
            customer=curent_user,
            recipe=recipe).exists()
        is_in_follow = Follows.objects.filter(
            subscriber=curent_user,
            author=recipe.author
        )
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
        purchases = Purchases.objects.filter(customer=curent_user)
        purchases_count = purchases.count()
    else:
        purchases_count = 0
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
                ingredient = Ingredients.objects.get(pk=key)
                amount = ing_for_recipes[key]
                ing_recipe = Ingredients_Recipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount
                )
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
            ing_id = Ingredients.objects.get(
                title=name_ing,
                dimension=units_ing).id
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
        ingr_recipe = Ingredients_Recipe.objects.get(
            recipe=recipe,
            ingredient=ingredient
        )
        ingredients_recipe.append(ingr_recipe)

    curent_user = request.user
    section = request.resolver_match.url_name
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
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
                ing_recipe = Ingredients_Recipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    amount=amount)
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


def get_all_ingredients_from_shoplist(request):
    curent_user = request.user
    purchases = Purchases.objects.filter(customer=curent_user)
    recipes = []
    for purchase in purchases:
        recipes.append(purchase.recipe)

    all_ingredients = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.all():
            ingr_recipe = Ingredients_Recipe.objects.get(
                recipe=recipe,
                ingredient=ingredient
            )
            cur_amount = ingr_recipe.amount
            cur_total_amount = all_ingredients.get(ingredient)
            if cur_total_amount is not None:
                summ_amounts = cur_total_amount + cur_amount
            else:
                summ_amounts = cur_amount
            all_ingredients[ingredient] = summ_amounts

    return all_ingredients


pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))


def download_shoplist(request):
    total_ingredients_dict = get_all_ingredients_from_shoplist(
        request)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont('Vera', 14)
    p.drawString(250, 800, "My SHOPLIST")
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
