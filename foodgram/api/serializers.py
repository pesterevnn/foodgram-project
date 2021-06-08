import sys
sys.path.append('recipes')
import recipes
from recipes.models import Purchases

from rest_framework import serializers


class PurchaseSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        user = self.context['request'].user
        recipe_id = self.context['view'].kwargs['recipe_id']
        purchase = user.purchases.filter(recipe_id=recipe_id)
        method = self.context['request'].method
        if purchase.count() != 0 and method == 'POST':
            raise serializers.ValidationError(
                f'Only one purchase must be to recipe with id:{recipe_id}'
            )
        return data

    class Meta:
        model = Purchases
