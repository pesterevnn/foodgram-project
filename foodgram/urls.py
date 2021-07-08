from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from recipes.views import index

handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),    
]

urlpatterns += [
    path(
        'fp/about-us/',
        views.flatpage,
        {'url': '/fp/about-us/'},
        name='about_us'
    ),
    path(
        'fp/about-techs/',
        views.flatpage,
        {'url': '/fp/about-techs/'},
        name='about_techs'
    ),
    path(
        'fp/about-brand/',
        views.flatpage,
        {'url': '/fp/about-brand/'},
        name='about_brand'
    ),
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
