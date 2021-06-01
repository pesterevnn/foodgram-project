from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Recipes, Purchases
#from ..users.models import User


def index(request):
    curent_user = request.user
    recipes = Recipes.objects.all()
    purchases = Purchases.objects.filter(customer = curent_user)
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases.count(),
        'section': section,
    }
    if curent_user.is_authenticated:
        return render(request, 'indexAuth.html', context)
    else:
        return render(request, 'indexNotAuth.html', context)

def favorite(request):
    curent_user = request.user
    #recipes_pks = curent_user.favorite_recipes.values_list('recipe', flat=True)
    #recipes = Recipes.objects.filter(pk__in=recipes_pks)
    recipes = Recipes.objects.filter(favorite_authors__user=curent_user)
    purchases = Purchases.objects.filter(customer = curent_user)
    paginator = Paginator(recipes, settings.PAGINATOR_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    section = request.resolver_match.url_name
    context = {
        'page': page,
        'recipes': recipes,
        'paginator': paginator,
        'user': curent_user,
        'purchases_count': purchases.count(),
        'section': section,
    }
    return render(request, 'favorite.html', context)

def profile(request, username):
    curent_user = request.user
    user = get_object_or_404(get_user_model(), username=username)
    recipes = Recipes.objects.filter(author=user)
    purchases = Purchases.objects.filter(customer = curent_user)
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
        'purchases_count': purchases.count(),
        'section': section,
    }
    return render(request, 'authorRecipe.html', context)    
