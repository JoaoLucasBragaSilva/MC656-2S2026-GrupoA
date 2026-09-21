from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def home(request):
    return render(request, 'accounts/home.html', {'site_name': 'E-Voting'})


