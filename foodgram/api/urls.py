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
    path('', include(v1_router.urls)),
]
