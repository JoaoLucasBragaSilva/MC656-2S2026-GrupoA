from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),

    # Custom urls
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/eleitor/', views.cadastro_eleitor, name='cadastro_eleitor'),
    path('cadastro/partido/', views.cadastro_partido, name='cadastro_partido'),
    path('login/', views.login_view, name='login'),        # ← NOVO
    path('logout/', views.logout_view, name='logout'),
]
