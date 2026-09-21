import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def home_url():
    return reverse('home')


def test_home_page_status_and_template(client, home_url):
    response = client.get(home_url)
    assert response.status_code == 200
    assert 'accounts/home.html' in [t.name for t in response.templates]


def test_home_page_context_site_name(client, home_url):
    response = client.get(home_url)
    site_name = response.context.get('site_name')
    assert site_name is not None
    assert site_name in response.content.decode()


def test_home_page_only_allows_get(client, home_url):
    response = client.post(home_url)
    assert response.status_code == 405  # Method Not Allowed


def test_home_page_renders_both_cards(client, home_url):
    response = client.get(home_url)
    content = response.content.decode()

    assert 'data-type="voter"' in content
    assert 'data-type="party"' in content

    assert content.index('data-type="voter"') < content.index('data-type="party"')


def test_home_page_login_link_present(client, home_url):
    response = client.get(home_url)
    content = response.content.decode()
    assert 'Fazer login' in content
    assert 'href="#"' in content 


def test_home_page_accessible_without_authentication(client, home_url):
    response = client.get(home_url)
    assert response.status_code == 200
    assert '_auth_user_id' not in client.session

def test_url_inexistente_retorna_404(client):
    response = client.get('/rota-que-nao-existe/')
    assert response.status_code == 404