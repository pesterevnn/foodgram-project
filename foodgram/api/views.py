from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from .serializers  import PurchaseSerializer
from .permissions import IsAuthUser, IsOwnerOrAdmin

import sys
sys.path.append('recipes')
import recipes
from recipes.models import Recipes

User = get_user_model()

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = (IsOwnerOrAdmin, IsAuthUser)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.purchases.all()

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipes, pk=self.kwargs.get('recipe_id'))
        serializer.save(customer=self.request.user, recipe=recipe)
