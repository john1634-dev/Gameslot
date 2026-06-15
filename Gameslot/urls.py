from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from slots.views import category_api, category_page, frontend, home_api

urlpatterns = [
    path('', frontend, name='frontend'),
    path('categories/<slug:slug>/', category_page, name='category_page'),
    path('api/home/', home_api, name='home_api'),
    path('api/categories/<slug:slug>/', category_api, name='category_api'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
