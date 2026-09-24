import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Eleitor, Partido

Usuario = get_user_model()


@pytest.mark.django_db
class TestHomeView:

    def test_home_carrega(self, client_django):
        response = client_django.get(reverse('accounts:home'))
        assert response.status_code == 200
        assert 'accounts/home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestCadastroEscolhaView:

    def test_pagina_escolha_carrega(self, client_django):
        response = client_django.get(reverse('accounts:cadastro'))
        assert response.status_code == 200
        assert 'accounts/cadastro.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestCadastroEleitorView:

    URL_NAME = 'accounts:cadastro_eleitor'

    def test_get_exibe_formulario(self, client_django):
        response = client_django.get(reverse(self.URL_NAME))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_post_dados_validos_cria_usuario(self, client_django, dados_eleitor_validos):
        response = client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        assert response.status_code == 302  # redirect após sucesso
        assert Usuario.objects.filter(email='joao.silva@example.com').exists()
        usuario = Usuario.objects.get(email='joao.silva@example.com')
        assert usuario.tipo == 'eleitor'
        assert Eleitor.objects.filter(usuario=usuario).exists()

    def test_post_dados_validos_loga_usuario(self, client_django, dados_eleitor_validos):
        client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        response = client_django.get(reverse('accounts:home'))
        assert response.context['user'].is_authenticated

    def test_post_cpf_invalido_nao_cria(self, client_django, dados_eleitor_validos):
        dados_eleitor_validos['cpf'] = '111.111.111-11'
        response = client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        assert response.status_code == 200  # re-renderiza com erro
        assert not Usuario.objects.filter(email='joao.silva@example.com').exists()
        assert response.context['form'].errors

    def test_post_email_duplicado(self, client_django, dados_eleitor_validos, usuario_eleitor):
        dados_eleitor_validos['email'] = usuario_eleitor.email
        response = client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        assert response.status_code == 200
        assert 'email' in response.context['form'].errors

    def test_post_senhas_diferentes(self, client_django, dados_eleitor_validos):
        dados_eleitor_validos['confirmar_senha'] = 'diferente123'
        response = client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        assert response.status_code == 200
        assert not Usuario.objects.filter(email='joao.silva@example.com').exists()

    def test_post_sem_termos(self, client_django, dados_eleitor_validos):
        dados_eleitor_validos.pop('termos')
        response = client_django.post(reverse(self.URL_NAME), dados_eleitor_validos)

        assert response.status_code == 200
        assert not Usuario.objects.filter(email='joao.silva@example.com').exists()


@pytest.mark.django_db
class TestCadastroPartidoView:

    URL_NAME = 'accounts:cadastro_partido'

    def test_get_exibe_formulario(self, client_django):
        response = client_django.get(reverse(self.URL_NAME))
        assert response.status_code == 200
        assert 'form' in response.context

    def test_post_dados_validos_cria_partido(self, client_django, dados_partido_validos):
        response = client_django.post(reverse(self.URL_NAME), dados_partido_validos)

        assert response.status_code == 302
        assert Usuario.objects.filter(email='contato@pdb.org.br').exists()
        usuario = Usuario.objects.get(email='contato@pdb.org.br')
        assert usuario.tipo == 'partido'
        assert Partido.objects.filter(sigla='PDB').exists()

    def test_post_cnpj_invalido_nao_cria(self, client_django, dados_partido_validos):
        dados_partido_validos['cnpj'] = '11.111.111/1111-11'
        response = client_django.post(reverse(self.URL_NAME), dados_partido_validos)

        assert response.status_code == 200
        assert not Usuario.objects.filter(email='contato@pdb.org.br').exists()

    def test_post_sigla_duplicada(self, client_django, dados_partido_validos, db):

        u = Usuario.objects.create_user(
            email='x@x.com', username='x', password='x12345678',
        )
        Partido.objects.create(
            usuario=u, nome='Outro', sigla='PDB',
            cnpj='11.222.333/0001-81',
            presidente='F', espectro='centro',
        )

        response = client_django.post(reverse(self.URL_NAME), dados_partido_validos)
        assert response.status_code == 200
        assert 'sigla' in response.context['form'].errors
