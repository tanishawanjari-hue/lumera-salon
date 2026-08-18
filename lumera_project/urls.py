from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'services/<int:category_id>/',
        views.category_services,
        name='category_services'
    ),

    path(
        'location/',
        views.location,
        name='location'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)