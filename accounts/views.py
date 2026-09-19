from django.shortcuts import render


def home(request):
    return render(request, 'accounts/home.html')

def cadastro(request):
    return render(request, 'accounts/cadastro.html')

def cadastro_votante(request):
    return render(request, 'accounts/cadastro_votante.html')

def cadastro_partido(request):
    return render(request, 'accounts/cadastro_partido.html')

def handler404(request, exception):
    """View customizada para erro 404."""
    return render(request, '404.html', status=404)

def handler500(request):
    """View customizada para erro 500."""
    return render(request, '500.html', status=500)
