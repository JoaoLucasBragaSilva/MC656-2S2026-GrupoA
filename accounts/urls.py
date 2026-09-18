from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/votante/', views.cadastro_votante, name='cadastro_votante'),
    path('cadastro/partido/', views.cadastro_partido, name='cadastro_partido'),
]