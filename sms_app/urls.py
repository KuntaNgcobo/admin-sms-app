from django.urls import path

from . import views

app_name = 'sms_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('sms_form/', views.sms_form, name='sms_form'),
]