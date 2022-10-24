from django.shortcuts import render
from .models import Perfil, Post


def index(request):
    template = 'posts/index.html'

    qtd_posts = Post.objects.count()
    qtd_perfis = Perfil.objects.count()

    context = {
        'qtd_posts': qtd_posts,
        'qtd_perfis': qtd_perfis,
    }

    return render(request, template, context)

