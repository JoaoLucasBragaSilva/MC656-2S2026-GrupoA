from django.shortcuts import redirect
from django.urls import NoReverseMatch, Resolver404, resolve, reverse


class LoginRequiredMiddleware:
    PUBLIC_PREFIXES = (
        '/admin/',
        '/login/',
        '/logout/',
        '/cadastro/',
        '/static/',
        '/media/',
        '/favicon.ico',
        '/robots.txt',
    )

    PUBLIC_EXACT = ('/',)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path in self.PUBLIC_EXACT:
            return self.get_response(request)

        if any(path.startswith(prefix) for prefix in self.PUBLIC_PREFIXES):
            return self.get_response(request)

        try:
            resolve(path)
        except Resolver404:
            return self.get_response(request)

        if not request.user.is_authenticated:
            try:
                login_url = reverse('accounts:login')
            except NoReverseMatch:
                login_url = '/login/'
            return redirect(f'{login_url}?next={path}')

        return self.get_response(request)
