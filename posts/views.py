from django.shortcuts import render
from .models import Perfil, Post
from .forms import PostForm


def index(request):
    template = 'posts/index.html'

    form = PostForm()
    qtd_posts = Post.objects.count()
    qtd_perfis = Perfil.objects.count()
    posts = Post.objects.all()
    perfis = Perfil.objects.all()

    context = {
        'qtd_posts': qtd_posts,
        'qtd_perfis': qtd_perfis,
        'posts': posts,
        'perfis': perfis,
        'form': form,
    }

    return render(request, template, context)

