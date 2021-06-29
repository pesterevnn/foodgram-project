from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('follow/', views.follow, name='follow'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path(
        'shoplist/download/',
        views.download_shoplist,
        name='download_shoplist'
    ),
    path('create_recipe/', views.create_or_edit_recipe, name='create_recipe'),
    path(
        'recipes/<int:recipe_id>/change_recipe/',
        views.create_or_edit_recipe,
        name='change_recipe'
    ),
    path(
        'recipes/<int:recipe_id>/change_recipe/del_recipe/',
        views.delete_recipe,
        name='del_recipe'
    ),
    path('recipes/<int:recipe_id>/', views.recipe, name='recipe'),
    path('<str:username>/', views.profile, name='profile'),
    path('recipes/api/', include('api.urls')),
    path('create_recipe/api/', include('api.urls')),
    path('change_recipe/api/', include('api.urls')),
    path('recipes/<int:recipe_id>/api/', include('api.urls')),
    path(
        'recipes/<int:recipe_id>/change_recipe/api/',
        include('api.urls')
    ),
    path('favorite/api/', include('api.urls')),
    path('follow/api/', include('api.urls')),
]
