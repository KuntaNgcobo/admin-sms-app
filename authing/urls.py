from django.urls import path

from . import views

app_name = 'authing'
urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('', views.logout_user, name='logout_user'),
]