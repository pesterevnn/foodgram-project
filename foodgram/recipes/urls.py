from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('follow/', views.follow, name='follow'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('<str:username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe, name='recipe'),
    path(
        '<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        '<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
    path(
        'recipes/<int:recipe_id>/add_purchase/',
        views.add_purchase,
        name='add_purchase'
    ),
    path(
        'recipes/<int:recipe_id>/del_purchase/',
        views.del_purchase,
        name='del_purchase'
    ),
]
