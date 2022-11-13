from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.registro, name='registro'),
    path('login/', views.logar, name='logar'),
    path('logout/', views.logout_usuario, name='logout'),
    path('perfis/', views.lista_perfis, name='lista_perfis'),
    path('perfil/<int:pk>/', views.perfil, name='perfil'),
    path('meus-posts/', views.meus_posts, name='meus_posts'),
    path('editar/<int:pk>/', views.editar_post, name="editar"),
    path('excluir/<int:pk>/', views.excluir_post, name='excluir'),
    path('troca-senha/', views.troca_senha, name='troca_senha'),
    path('likes/<int:post_id>', views.like, name='like'),
]
