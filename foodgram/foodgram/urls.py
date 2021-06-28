from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path

handler404 = 'recipes.views.page_not_found'
handler500 = 'recipes.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('favorite/api/', include('api.urls')),
    path('follow/api/', include('api.urls')),
    path('recipes/api/', include('api.urls')),
    path('create_recipe/api/', include('api.urls')),
    path('change_recipe/api/', include('api.urls')),
    path('recipes/<int:recipe_id>/api/', include('api.urls')),
    path(
        'recipes/<int:recipe_id>/change_recipe/api/',
        include('api.urls')
    ),
    path('<str:username>/api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
