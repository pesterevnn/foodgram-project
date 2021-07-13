from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import (Ingredient, IngredientRecipe, Purchase, Recipe, Tag,
                     UsersTag)


def get_users_tags(request, user=None):
    if user is None:
        user = request.user
    users_tags = user.userstags.all()
    return users_tags


def get_tags_ids(post_dict):
    tags_ids = []
    if post_dict.get('breakfast'):
        tags_ids.append(get_object_or_404(Tag, tag='breakfast').id)
    if post_dict.get('lunch'):
        tags_ids.append(get_object_or_404(Tag, tag='lunch').id)
    if post_dict.get('dinner'):
        tags_ids.append(get_object_or_404(Tag, tag='dinner').id)
    return tags_ids


def get_all_ingredients_from_shoplist(request):
    curent_user = request.user
    purchases = Purchase.objects.filter(customer=curent_user)
    recipes = []
    for purchase in purchases:
        recipes.append(purchase.recipe)

    all_ingredients = {}
    for recipe in recipes:
        for ingredient in recipe.ingredients.all():
            ingr_recipe = get_object_or_404(
                IngredientRecipe,
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


def set_active_users_tags(request, user=None):
    if user is None:
        user = request.user
    tags = Tag.objects.all()
    users_tags = []
    if user.is_authenticated:
        for tag in tags:
            values_for_update = {
                'user': user,
                'tag': tag,
                'active': True
            }
            users_tag, created = UsersTag.objects.update_or_create(
                user=user,
                tag=tag,
                defaults=values_for_update
            )
            users_tags.append(users_tag)
    return users_tags


def get_actual_users_tags(request, tag_click, user=None):
    if user is None:
        curent_user = request.user
    else:
        curent_user = user
    users_tags = []
    if tag_click is not None:
        tag_id = get_object_or_404(Tag, tag=tag_click).id
        tag = get_object_or_404(
            UsersTag,
            tag=tag_id,
            user=curent_user
        )
        tag_swch = request.GET.get('swch')
        if tag_swch == 'off':
            tag.active = False
        else:
            tag.active = True
        tag.save()
        users_tags = curent_user.userstags.all()
    elif request.GET.get('page') is None:
        users_tags = set_active_users_tags(request, curent_user)
    else:
        users_tags = get_users_tags(request, curent_user)
    return users_tags


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


def get_ingredients_for_recipe(post_dict):
    ingredients_recipe_dic = {}
    for key in post_dict.keys():
        if key[:14] == 'nameIngredient':
            index = key[-1]
            name_ing = post_dict[key]
            value_ing = post_dict[f'valueIngredient_{index}']
            units_ing = post_dict[f'unitsIngredient_{index}']
            ing_id = get_object_or_404(
                Ingredient,
                title=name_ing,
                dimension=units_ing).id
            ingredients_recipe_dic[ing_id] = value_ing
    return ingredients_recipe_dic


def get_filtered_recipes_by_tags(request, filtered_id_list=None,
                                 user=None):
    tag_click = request.GET.get('tag')
    if request.user.is_authenticated:
        users_tags = get_actual_users_tags(request, tag_click)
    else:
        cur_user = get_object_or_404(get_user_model(), username='anonymus')
        users_tags = get_actual_users_tags(request, tag_click, user=cur_user)
    filtered_tags_id = []
    for item in users_tags:
        if item.active:
            filtered_tags_id.append(item.tag.id)
    if filtered_id_list is None:
        recipes = Recipe.objects.filter(
            tags__in=filtered_tags_id).distinct()
    else:
        recipes = Recipe.objects.filter(
            tags__in=filtered_tags_id,
            pk__in=filtered_id_list).distinct()
    if user is not None:
        recipes = Recipe.objects.filter(
            author=user,
            tags__in=filtered_tags_id).distinct()
    return recipes
