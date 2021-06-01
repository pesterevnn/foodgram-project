from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorite/', views.favorite, name='favorite'),
    path('<str:username>/', views.profile, name='profile'),
]
