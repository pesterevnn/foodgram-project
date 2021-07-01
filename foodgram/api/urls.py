from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteRecipeViewSet, IngredientViewSet, PurchaseViewSet,
                    SubscribeViewSet)

v1_router = DefaultRouter()
v1_router.register(
    'purchases',
    PurchaseViewSet,
    basename='add purchase'
)
v1_router.register(
    'purchases/<int:pk>',
    PurchaseViewSet,
    basename='remove purchase'
)
v1_router.register(
    r'favorites',
    FavoriteRecipeViewSet,
    basename='favorites'
)
v1_router.register(
    r'subscriptions',
    SubscribeViewSet,
    basename='add subscriptions'
)
v1_router.register(
    r'subscriptions/<int:pk>',
    SubscribeViewSet,
    basename='remove subscription'
)
v1_router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('favorite/api/', include(v1_router.urls)),
    path('', include(v1_router.urls)),
]

#    path('recipes/api/', include('api.urls')),
#    path('favorite/api/', include('api.urls')),
#    path('follow/api/', include('api.urls')),
#    path('create_recipe/api/', include('api.urls')),
#    path('change_recipe/api/', include('api.urls')),
#    path(
#        'recipes/<int:recipe_id>/change_recipe/api/',
#        include('api.urls')
#    ),
#    path('<str:username>/api/', include('api.urls')),
#    path('recipes/<int:recipe_id>/api/', include('api.urls')),
#v1_router.register(
#    r'recipes/<int:recipe_id>',
#    FavoriteRecipeViewSet,
#    basename='favorites for recipe'
#)