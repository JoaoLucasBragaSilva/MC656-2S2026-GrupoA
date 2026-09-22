from django import forms
from django.contrib.auth import get_user_model

from .validators import validar_cnpj, validar_cpf

Usuario = get_user_model()


class CadastroEleitorForm(forms.Form):
    nome = forms.CharField(max_length=150)
    cpf = forms.CharField(max_length=14)
    nascimento = forms.DateField()
    email = forms.EmailField()
    senha = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput)
    termos = forms.BooleanField()

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not validar_cpf(cpf):
            raise forms.ValidationError('CPF inválido.')
        return cpf

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado.')
        return email

    def clean(self):
        cleaned = super().clean()
        senha = cleaned.get('senha')
        confirmar = cleaned.get('confirmar_senha')
        if senha and confirmar and senha != confirmar:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')
        return cleaned

    def save(self):
        from .models import Eleitor
        dados = self.cleaned_data
        username_base = dados['email'].split('@')[0]
        username = username_base
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f'{username_base}{contador}'
            contador += 1

        usuario = Usuario.objects.create_user(
            email=dados['email'],
            username=username,
            password=dados['senha'],
            first_name=dados['nome'].split()[0],
            tipo='eleitor',
        )
        Eleitor.objects.create(
            usuario=usuario,
            cpf=dados['cpf'],
            data_nascimento=dados['nascimento'],
        )
        return usuario


class CadastroPartidoForm(forms.Form):
    nome_partido = forms.CharField(max_length=100)
    sigla = forms.CharField(max_length=10)
    cnpj = forms.CharField(max_length=18)
    email_partido = forms.EmailField()
    telefone = forms.CharField(max_length=20, required=False)
    presidente = forms.CharField(max_length=100)
    espectro = forms.ChoiceField(choices=[
        ('esquerda', 'Esquerda'),
        ('centro-esquerda', 'Centro-esquerda'),
        ('centro', 'Centro'),
        ('centro-direita', 'Centro-direita'),
        ('direita', 'Direita'),
    ])
    senha_partido = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirmar_senha_partido = forms.CharField(widget=forms.PasswordInput)
    termos_partido = forms.BooleanField()

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        if not validar_cnpj(cnpj):
            raise forms.ValidationError('CNPJ inválido.')
        return cnpj

    def clean_sigla(self):
        from .models import Partido
        sigla = self.cleaned_data['sigla'].upper()
        if Partido.objects.filter(sigla=sigla).exists():
            raise forms.ValidationError('Sigla já cadastrada.')
        return sigla

    def clean_email_partido(self):
        email = self.cleaned_data['email_partido'].lower()
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado.')
        return email

    def clean(self):
        cleaned = super().clean()
        s = cleaned.get('senha_partido')
        c = cleaned.get('confirmar_senha_partido')
        if s and c and s != c:
            self.add_error('confirmar_senha_partido', 'As senhas não coincidem.')
        return cleaned

    def save(self):
        from .models import Partido
        dados = self.cleaned_data
        sigla = dados['sigla'].upper()
        username = sigla.lower()
        base = username
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f'{base}{contador}'
            contador += 1

        usuario = Usuario.objects.create_user(
            email=dados['email_partido'],
            username=username,
            password=dados['senha_partido'],
            tipo='partido',
            telefone=dados.get('telefone', ''),
        )
        Partido.objects.create(
            usuario=usuario,
            nome=dados['nome_partido'],
            sigla=sigla,
            cnpj=dados['cnpj'],
            presidente=dados['presidente'],
            espectro=dados['espectro'],
        )
        return usuario
