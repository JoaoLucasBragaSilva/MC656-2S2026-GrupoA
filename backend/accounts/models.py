from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('eleitor', 'eleitor'),
        ('partido', 'Partido'),
        ('admin', 'Administrador'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='eleitor')
    telefone = models.CharField(max_length=20, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ClassVar[list[str]] = ['username']

    def __str__(self):
        return f'{self.email} ({self.get_tipo_display()})'


class Eleitor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='eleitor')
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    titulo_eleitor = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'eleitor: {self.usuario.email}'


class Partido(models.Model):
    ESPECTRO_CHOICES = (
        ('esquerda', 'Esquerda'),
        ('centro-esquerda', 'Centro-esquerda'),
        ('centro', 'Centro'),
        ('centro-direita', 'Centro-direita'),
        ('direita', 'Direita'),
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='partido')
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=10, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    presidente = models.CharField(max_length=100)
    espectro = models.CharField(max_length=20, choices=ESPECTRO_CHOICES)
    logo = models.ImageField(upload_to='partidos/logos/', blank=True, null=True)

    def __str__(self):
        return f'{self.sigla} - {self.nome}'
