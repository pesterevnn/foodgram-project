import sys
sys.path.append('recipes')
import recipes
from recipes.models import Purchases, FavoriteRecipes

from rest_framework import serializers


class PurchaseSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Purchases
        fields = '__all__'
#        exclude = ('recipe',)

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    recipe = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = FavoriteRecipes
        fields = '__all__'
