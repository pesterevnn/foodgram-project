from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Recipes, Purchases, Follows


def index(request):
    curent_user = request.user
    recipes = Recipes.objects.all()
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
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
    }
    return render(request, 'index.html', context)

def favorite(request):
    curent_user = request.user
    recipes = Recipes.objects.filter(favorite_authors__user=curent_user)
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
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
    }
    return render(request, 'favorite.html', context)

def profile(request, username):
    curent_user = request.user
    user = get_object_or_404(get_user_model(), username=username)
    recipes = Recipes.objects.filter(author=user)
    if request.user.is_authenticated:
        purchases = Purchases.objects.filter(customer = curent_user)
        purchases_count = purchases.count()
    else:
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
