from rest_framework import serializers

from recipes.models import FavoriteRecipe, Follow, Ingredient, Purchase


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
        model = Purchase
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
        model = FavoriteRecipe
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
        model = Follow
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(many=False)

    class Meta:
        model = Ingredient
        fields = '__all__'
