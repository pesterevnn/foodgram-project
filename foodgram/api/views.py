from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import viewsets
from rest_framework import filters
from .serializers  import PurchaseSerializer, FavoriteRecipeSerializer
from .serializers  import SubscribeSerializer, IngredientSerializer
from .permissions import IsAuthUser, IsOwnerOrAdmin

from rest_framework import status
from rest_framework.response import Response

import sys
sys.path.append('recipes')
import recipes
from recipes.models import Recipes, Purchases, FavoriteRecipes, Follows, Ingredients

User = get_user_model()

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthUser,)

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.purchases.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipes, pk=self.request.data['id'])
        serializer.save(customer=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, pk=self.kwargs.get("pk"))
        instance = Purchases.objects.filter(customer=self.request.user, recipe=recipe)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipes.objects.all()
    serializer_class = FavoriteRecipeSerializer

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.favorite_recipes.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipes, pk=self.request.data['id'])
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, pk=self.kwargs.get("pk"))
        instance = FavoriteRecipes.objects.filter(user=self.request.user, recipe=recipe)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Follows.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.subscriber.all()

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.request.data['id'])
        serializer.save(subscriber=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs.get("pk"))
        instance = Follows.objects.filter(subscriber=self.request.user, author=author)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title',]
