from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import FavoriteRecipe, Follow, Ingredient, Purchase, Recipe
from rest_framework import filters, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .permissions import IsAuthUser
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscribeSerializer)

User = get_user_model()


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = []
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.purchases.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe,
            pk=self.request.data['id']
        )
        serializer.save(customer=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        instance = Purchase.objects.filter(
            customer=self.request.user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = [IsAuthUser]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.favorite_recipes.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(
            Recipe,
            pk=self.request.data['id']
        )
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
        instance = FavoriteRecipe.objects.filter(
            user=self.request.user,
            recipe=recipe
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = []
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        curent_user = self.request.user
        return curent_user.subscriber.all()

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.request.data['id'])
        serializer.save(subscriber=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs.get('pk'))
        instance = Follow.objects.filter(
            subscriber=self.request.user,
            author=author
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = []
    authentication_classes = []
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]
