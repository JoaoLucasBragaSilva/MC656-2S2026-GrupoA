import pytest


@pytest.mark.django_db
class TestNavegacaoBasica:

    def test_home_responde_200(self, client_django):
        response = client_django.get('/')
        assert response.status_code == 200

    def test_cadastro_responde_200(self, client_django):
        response = client_django.get('/cadastro/')
        assert response.status_code == 200

    def test_cadastro_eleitor_responde_200(self, client_django):
        response = client_django.get('/cadastro/eleitor/')
        assert response.status_code == 200

    def test_cadastro_partido_responde_200(self, client_django):
        response = client_django.get('/cadastro/partido/')
        assert response.status_code == 200

    def test_url_inexistente_retorna_404(self, client_django):
        response = client_django.get('/rota-que-nao-existe/')
        assert response.status_code == 404
