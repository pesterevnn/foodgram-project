from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from .models import (FavoriteRecipe, Follow, Ingredient, IngredientRecipe,
                     Purchase, Recipe, Tag)


class FallowAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'author')
    search_fields = ('subscriber', 'author')


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'recipe')
    search_fields = ('customer',)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    fk_name = "recipe"
    max_num = 3


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'pub_date')
    inlines = [
        IngredientInline,
    ]


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'description', 'color')


class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Follow, FallowAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Tag, TagAdmin)
