from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (PurchaseViewSet,)


v1_router = DefaultRouter()
v1_router.register('purchases', PurchaseViewSet, basename='purchases')

#v1_router.register(
#    r'pecipes/(?P<recipe_id>\d+)/purchases/',
#    PurchaseViewSet,
#    basename='current purchase for recipe'
#)

urlpatterns = [
    path('v1/', include(v1_router.urls),),
]