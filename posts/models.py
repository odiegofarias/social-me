from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    conteudo = models.CharField(max_length=140)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.DO_NOTHING,
    )
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "posts"
        ordering = ['-data_criacao']


    def __str__(self) -> str:
        return (
            f"ID: {self.id}, "
            f"{self.autor} "
            f"({self.data_criacao: %d/%m/%Y %H:%M}).  "
            f"{self.conteudo[:30]}..."
        )

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    seguidores = models.ManyToManyField(
        "self",
        related_name="seguido_por",
        symmetrical=False,
        blank=True,
    )
    imagem = models.ImageField(upload_to='perfil/imagens/%Y/%m/%d/', blank=True, default='')
    favorita = models.ManyToManyField(Post)

    def __str__(self) -> str:
        return self.usuario.username

    class Meta:
        verbose_name_plural = 'perfis'


@receiver(post_save, sender=User)
def cria_perfil(sender, instance, created, **kwargs):
    if created:
        perfil_usuario = Perfil(usuario=instance)
        perfil_usuario.save()

        perfil_usuario.seguidores.add(instance.perfil)
        perfil_usuario.save()