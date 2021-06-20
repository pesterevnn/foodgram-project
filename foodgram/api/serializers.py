import sys
sys.path.append('recipes')
import recipes
from recipes.models import Purchases, FavoriteRecipes, Follows, Ingredients

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


class SubscribeSerializer(serializers.ModelSerializer):
    subscriber = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Follows
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('title', 'dimension',)
