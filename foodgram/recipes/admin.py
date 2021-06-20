from django.contrib import admin

from .models import Ingredients, Recipes, Ingredients_Recipe
from .models import Follows, FavoriteRecipes, Purchases, Tags


class FallowsAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author')
    search_fields = ('subscriber', 'author')


class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)


class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('customer', 'recipe')
    search_fields = ('customer',)


class IngredientsInline(admin.TabularInline):
    model = Ingredients_Recipe
    fk_name = "recipe"
    max_num = 3


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pub_date')
    inlines = [
        IngredientsInline,
    ]

class IngredientsRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'description', 'color')

admin.site.register(Ingredients)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredients_Recipe, IngredientsRecipeAdmin)
admin.site.register(Follows, FallowsAdmin)
admin.site.register(Purchases, PurchasesAdmin)
admin.site.register(FavoriteRecipes, FavoriteRecipesAdmin)
admin.site.register(Tags, TagsAdmin)
