from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),  # все адреса из приложения news подключаем к urls проекта
    path('accounts/', include('allauth.urls')),
    path('', include('protect.urls')),
]
