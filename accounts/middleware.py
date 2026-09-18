from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


class LoginRequiredMiddleware:
    """
    Protege rotas privadas exigindo autenticação.
    
    Por padrão, libera:
    - /admin/          (login do admin)
    - /login/          (login do sistema)
    - /cadastro/       (e subrotas)
    - /               (home)
    - arquivos estáticos e media
    - a própria página de login
    
    Qualquer outra rota exige `request.user.is_authenticated`.
    """

    # Rotas públicas (prefixos que NÃO exigem login)
    PUBLIC_PREFIXES = (
        '/admin/',
        '/login/',
        '/logout/',
        '/cadastro/',
        '/static/',
        '/media/',
        '/favicon.ico',
    )

    # Rotas públicas exatas
    PUBLIC_EXACT = (
        '/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Libera rotas exatas
        if path in self.PUBLIC_EXACT:
            return self.get_response(request)

        # Libera prefixos públicos
        if any(path.startswith(prefix) for prefix in self.PUBLIC_PREFIXES):
            return self.get_response(request)

        # Se o usuário não está logado, redireciona para login
        if not request.user.is_authenticated:
            login_url = reverse('accounts:login')
            return redirect(f'{login_url}?next={path}')

        return self.get_response(request)