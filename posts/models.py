from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    seguidores = models.ManyToManyField(
        "self",
        related_name="seguido_por",
        symmetrical=False,
        blank=True,
    )

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


class Post(models.Model):
    conteudo = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name_plural = "posts"


    def __str__(self) -> str:
        return (
            f"{self.autor} "
            f"({self.data_criacao: %d/%m/%Y %H:%M}).  "
            f"{self.conteudo[:30]}..."
        )