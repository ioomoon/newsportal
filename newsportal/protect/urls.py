from django.urls import path
from .views import ProtectView, BaseRegisterView
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me


urlpatterns = [
    path('', ProtectView.as_view()),
    path('logout/', LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('signup/',
         BaseRegisterView.as_view(template_name='signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
]
