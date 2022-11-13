from django.http import Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Perfil, Post, Likes
from .forms import LoginForm, PostForm, RegisterForm, NovaSenhaForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    posts = Post.objects.all()

    return render(request, 'posts/index.html', {'posts': posts})


def dashboard(request):
    template = 'posts/dashboard.html'
    form = PostForm(request.POST or None)
    perfis = Perfil.objects.all()

    if request.method == "POST":
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.autor = request.user
            mensagem.save()

            return redirect("posts:dashboard")
    
    posts_pessoas_que_sigo = Post.objects.filter(
        autor__perfil__in=request.user.perfil.seguidores.all()
    ).exclude(autor=request.user).order_by('-data_criacao')


    context = {
        'form': form,
        'seguindo_posts': posts_pessoas_que_sigo,
        'perfis': perfis,
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

        return redirect('posts:perfil', pk=pk)

    context = {
        'perfil': perfil,
        'meus_posts': meus_posts,
    }

    return render(request, template, context)


def meus_posts(request):
    template = 'posts/meus_posts.html'

    posts = Post.objects.filter(autor=request.user)

    return render(request, template, {'posts': posts})


def editar_post(request, pk):
    template = 'posts/editar_post.html'
    post = Post.objects.get(pk=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:perfil', pk=request.user.id)
    
    context = {
        'form': form
    }

    return render(request, template, context)



def excluir_post(request, pk):
    template = 'posts/excluir_post.html'
    post = Post.objects.get(pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('posts:perfil', pk=request.user.id)

    context = {'post': post}

    return render(request, template, context)


@login_required(login_url='posts:logar', redirect_field_name='next')
def troca_senha(request):
    template = 'posts/reset_password.html'
    user = request.user

    if request.method == "POST":
        form = NovaSenhaForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Senha trocada com sucesso")
            
            return redirect('posts:logar')
    
    form = NovaSenhaForm(user)

    return render(request, template, {'form': form})


def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Likes.objects.create(user=user, post=post)
        current_likes += 1
    else:
        liked = Likes.objects.filter(user=user, post=post).delete()
        current_likes -= 1
    
    post.likes = current_likes
    post.save()

    return redirect('posts:dashboard')


def favorita(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    perfil = Perfil.objects.get(usuario=user)

    if perfil.favorita.filter(id=post_id).exists():
        perfil.favorita.remove(post)
    else:
        perfil.favorita.add(post)

    return redirect('posts:dashboard')


