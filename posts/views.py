from django.http import Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Perfil, Post
from .forms import LoginForm, PostForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index(request):
    template = 'posts/index.html'

    
    qtd_posts = Post.objects.count()
    qtd_perfis = Perfil.objects.count()
    posts = Post.objects.all()
    perfis = Perfil.objects.all()

    form = PostForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.autor = request.user
            mensagem.save()

            return redirect("posts:index")

    

    context = {
        'qtd_posts': qtd_posts,
        'qtd_perfis': qtd_perfis,
        'posts': posts,
        'perfis': perfis,
        'form': form,
    }

    return render(request, template, context)


def registro(request):
    template = 'posts/registro.html'

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            return redirect('posts:index')

    form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


def login(request):
    template = 'posts/login.html'
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('posts:index')
            else:
                return HttpResponse('Deu RUIM')
    
    return render(request, template, {'form': form})





