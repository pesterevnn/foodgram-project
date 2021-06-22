from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteRecipeViewSet, IngredientViewSet,
                    PurchaseViewSet, SubscribeViewSet)

v1_router = DefaultRouter()
v1_router.register(
    'purchases',
    PurchaseViewSet,
    basename='purchases'
)
v1_router.register(
    'favorites',
    FavoriteRecipeViewSet,
    basename='favorites'
)
v1_router.register(
    'subscriptions',
    SubscribeViewSet,
    basename='subscriptions'
)
v1_router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('v1/', include(v1_router.urls),),
]
