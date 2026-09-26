from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('accounts:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:home')

@require_GET
def home(request):
    context = {
        'site_name': 'Nome do Projeto',
    }
    return render(request, 'accounts/home.html', context)

def cadastro(request):
    return render(request, 'accounts/cadastro.html')

def cadastro_eleitor(request):
    from .forms import CadastroEleitorForm

    if request.method == 'POST':
        form = CadastroEleitorForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('accounts:home')
    else:
        form = CadastroEleitorForm()

    return render(request, 'accounts/cadastro_eleitor.html', {'form': form})

def cadastro_partido(request):
    from .forms import CadastroPartidoForm

    if request.method == 'POST':
        form = CadastroPartidoForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('accounts:home')
    else:
        form = CadastroPartidoForm()

    return render(request, 'accounts/cadastro_partido.html', {'form': form})

def handler404(request, exception):
    """View customizada para erro 404."""
    return render(request, '404.html', status=404)

def handler500(request):
    """View customizada para erro 500."""
    return render(request, '500.html', status=500)
