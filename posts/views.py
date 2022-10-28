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

    form = PostForm(request.POST or None)

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


def logar(request):
    template = 'posts/login.html'

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data.get('username', ''),
                password = form.cleaned_data.get('password', ''),    
            )

            if user is not None:
                messages.success(request, 'Você logou!')
                login(request, user)
                return redirect('posts:index')
            else:
                messages.error(request, 'Credenciais inválidas')
        else:
            messages.error(request, 'Usuário ou senha incorreto')

    form = LoginForm()

    return render(request, template, {'form': form})


def logout_usuario(request):
    logout(request)
    return redirect('posts:index')


def lista_perfis(request):
    template = 'posts/perfis.html'

    perfis = Perfil.objects.exclude(usuario=request.user)
    return render(request, template, {'perfis': perfis})


def perfil(request, pk):
    template = 'posts/perfil.html'
    if not hasattr(request.user, 'perfil'):
        sem_perfil = Perfil(usuario=request.user)
        sem_perfil.save()

    perfil = Perfil.objects.get(pk=pk)
    meus_posts = Post.objects.all().filter(autor=request.user)

    # print(perfil)
    if request.method == "POST":
        perfil_atual = request.user.perfil
        acao = request.POST.get('seguir')

        if acao == 'seguir':
            perfil_atual.seguidores.add(perfil)
        elif acao == 'deixar-seguir':
            perfil_atual.seguidores.remove(perfil)

        perfil_atual.save()

    context = {
        'perfil': perfil,
        'meus_posts': meus_posts,
    }
    return render(request, template, context)


def meus_posts(request):
    template = 'posts/meus_posts.html'

    posts = Post.objects.filter(autor=request.user)

    return render(request, template, {'posts': posts})





