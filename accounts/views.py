from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

def cadastro(request):
    return render(request, 'accounts/cadastro.html')

def cadastro_votante(request):
    return render(request, 'accounts/cadastro_votante.html')

def cadastro_partido(request):
    return render(request, 'accounts/cadastro_partido.html')