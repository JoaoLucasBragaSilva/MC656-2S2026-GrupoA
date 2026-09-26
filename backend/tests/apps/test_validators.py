import pytest

from accounts.validators import validar_cnpj, validar_cpf


class TestValidarCPF:

    @pytest.mark.parametrize('cpf', [
        '52998224725',
        '529.982.247-25',
        '111.444.777-35',
        '11144477735',
    ])
    def test_cpf_valido(self, cpf):
        assert validar_cpf(cpf) is True

    @pytest.mark.parametrize('cpf', [
        '11111111111',
        '00000000000',
        '12345678900',
        '123',
        '',
        'abc.def.ghi-jk',
    ])
    def test_cpf_invalido(self, cpf):
        assert validar_cpf(cpf) is False


class TestValidarCNPJ:

    @pytest.mark.parametrize('cnpj', [
        '11222333000181',
        '11.222.333/0001-81',
    ])
    def test_cnpj_valido(self, cnpj):
        assert validar_cnpj(cnpj) is True

    @pytest.mark.parametrize('cnpj', [
        '11111111111111',
        '00000000000000',
        '12345678901234',
        '123',
        '',
    ])
    def test_cnpj_invalido(self, cnpj):
        assert validar_cnpj(cnpj) is False
