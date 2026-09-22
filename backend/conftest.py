import os

import django
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
Usuario = get_user_model()


@pytest.fixture
def client_django():
    """Client de teste do Django (não DRF)."""
    return Client()


@pytest.fixture
def dados_eleitor_validos():
    """Payload válido para formulário de cadastro de eleitor."""
    return {
        'nome': 'João da Silva',
        'cpf': '529.982.247-25',
        'nascimento': '1990-05-15',
        'email': 'joao.silva@example.com',
        'senha': 'senhaSegura123',
        'confirmar_senha': 'senhaSegura123',
        'termos': 'on',
    }


@pytest.fixture
def dados_partido_validos():
    """Payload válido para formulário de cadastro de partido."""
    return {
        'nome_partido': 'Partido Democrático Brasileiro',
        'sigla': 'PDB',
        'cnpj': '11.222.333/0001-81',
        'email_partido': 'contato@pdb.org.br',
        'telefone': '(11) 3333-4444',
        'presidente': 'Carlos Andrade',
        'espectro': 'centro',
        'senha_partido': 'senhaSegura123',
        'confirmar_senha_partido': 'senhaSegura123',
        'termos_partido': 'on',
    }


@pytest.fixture
def usuario_eleitor(db):
    """Cria e persiste um usuário eleitor."""
    return Usuario.objects.create_user(
        email='eleitor@example.com',
        username='eleitor',
        password='senha12345',
        tipo='eleitor',
    )


@pytest.fixture
def usuario_logado(client_django, usuario_eleitor):
    """Client autenticado como eleitor."""
    client_django.force_login(usuario_eleitor)
    return client_django
