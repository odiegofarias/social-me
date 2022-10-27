from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registro, name='registro'),
    path('login/', views.logar, name='logar'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfis/', views.lista_perfis, name='lista_perfis'),
    path('perfil/<int:pk>', views.perfil, name='perfil'),
]
