from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from accounts.models import Eleitor, Partido

Usuario = get_user_model()


@pytest.mark.django_db
class TestUsuarioModel:

    def test_criar_usuario_eleitor(self):
        u = Usuario.objects.create_user(
            email='teste@example.com',
            username='teste',
            password='senha12345',
            tipo='eleitor',
        )
        assert u.email == 'teste@example.com'
        assert u.tipo == 'eleitor'
        assert u.check_password('senha12345') is True
        assert u.is_active is True

    def test_criar_usuario_partido(self):
        u = Usuario.objects.create_user(
            email='partido@example.com',
            username='partido',
            password='senha12345',
            tipo='partido',
        )
        assert u.tipo == 'partido'

    def test_str_retorna_email_e_tipo(self):
        u = Usuario.objects.create_user(
            email='teste@example.com',
            username='teste',
            password='senha12345',
            tipo='partido',
        )
        texto = str(u)
        assert 'teste@example.com' in texto

        assert 'Partido' in texto or 'partido' in texto.lower()

    def test_email_unico(self):
        Usuario.objects.create_user(
            email='unico@example.com', username='u1', password='senha12345',
        )
        with pytest.raises(IntegrityError):
            Usuario.objects.create_user(
                email='unico@example.com', username='u2', password='senha12345',
            )


@pytest.mark.django_db
class TestEleitorModel:

    def test_criar_eleitor(self, usuario_eleitor):
        eleitor_obj = Eleitor.objects.create(
            usuario=usuario_eleitor,
            cpf='529.982.247-25',
            data_nascimento=date(1990, 5, 15),
        )
        assert eleitor_obj.usuario == usuario_eleitor
        assert eleitor_obj.cpf == '529.982.247-25'
        assert eleitor_obj.data_nascimento == date(1990, 5, 15)

    def test_str_contem_email(self, usuario_eleitor):
        eleitor_obj = Eleitor.objects.create(
            usuario=usuario_eleitor,
            cpf='529.982.247-25',
            data_nascimento=date(1990, 5, 15),
        )
        assert 'eleitor@example.com' in str(eleitor_obj)


@pytest.mark.django_db
class TestPartidoModel:

    def test_criar_partido(self):
        u = Usuario.objects.create_user(
            email='p@example.com', username='p', password='x12345678',
            tipo='partido',
        )
        partido = Partido.objects.create(
            usuario=u,
            nome='Partido Teste',
            sigla='PT',
            cnpj='11.222.333/0001-81',
            presidente='Fulano de Tal',
            espectro='centro',
        )
        assert partido.sigla == 'PT'
        assert partido.nome == 'Partido Teste'

    def test_str_contem_sigla(self):
        u = Usuario.objects.create_user(
            email='p@example.com', username='p', password='x12345678',
            tipo='partido',
        )
        partido = Partido.objects.create(
            usuario=u, nome='Partido X', sigla='PX',
            cnpj='11.222.333/0001-81',
            presidente='F', espectro='centro',
        )
        assert 'PX' in str(partido)
