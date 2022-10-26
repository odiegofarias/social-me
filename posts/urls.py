from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
]
