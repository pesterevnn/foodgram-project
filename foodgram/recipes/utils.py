from .models import Ingredients, Ingredients_Recipe, Purchases, Tags, UsersTags


def get_usertags(request):
    user = request.user
    users_tags = user.userstags.all()
    return users_tags


def get_tags_ids(post_dict):
    tags_ids = []
    if post_dict.get('breakfast'):
        tags_ids.append(Tags.objects.get(tag='breakfast').id)
    if post_dict.get('lunch'):
        tags_ids.append(Tags.objects.get(tag='lunch').id)
    if post_dict.get('dinner'):
        tags_ids.append(Tags.objects.get(tag='dinner').id)
    return tags_ids


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


def set_active_userstags(request):
    user = request.user
    tags = Tags.objects.all()
    users_tags = []
    if user.is_authenticated:
        for tag in tags:
            values_for_update = {
                'user': user,
                'tag': tag,
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
            value_ing = post_dict[f"valueIngredient_{index}"]
            units_ing = post_dict[f"unitsIngredient_{index}"]
            ing_id = Ingredients.objects.get(
                title=name_ing,
                dimension=units_ing).id
            ingredients_recipe_dic[ing_id] = value_ing
    return ingredients_recipe_dic
