from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('follow/', views.follow, name='follow'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path('<str:username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe, name='recipe'),
]
