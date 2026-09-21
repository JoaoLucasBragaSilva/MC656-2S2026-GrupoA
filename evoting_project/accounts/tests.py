from django.test import TestCase
from django.urls import reverse

class HomeViewTest(TestCase):
  def test_home_page(self):
    response = self.client.get(reverse('home'))  # ajuste o nome da url

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'accounts/home.html')

    # Textos principais
    self.assertContains(response, "Escolha seu tipo de cadastro")
    self.assertContains(response, "Eleitor")
    self.assertContains(response, "Partido Político")
    self.assertContains(response, "Pessoa Física")
    self.assertContains(response, "Pessoa Jurídica")

    # Footer de login
    self.assertContains(response, "Já tem uma conta?")
    self.assertContains(response, "Fazer login")

    # Estrutura dos cards
    self.assertContains(response, 'data-type="voter"')
    self.assertContains(response, 'data-type="party"')
    self.assertContains(response, 'class="card-stripe voter-stripe"')
    self.assertContains(response, 'class="card-stripe party-stripe"')

    # CSS carregado
    self.assertContains(response, 'home.css')