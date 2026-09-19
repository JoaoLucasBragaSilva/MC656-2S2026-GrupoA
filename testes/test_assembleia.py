import pytest

from apuracao.maioria_simples import (
    apurar_votacao,
    calcular_maioria_qualificada_ponderada,
    calcular_maioria_simples_assembleia_condominio,
    calcular_maioria_simples_ponderada,
    calcular_proporcao_ideal_assembleia_condominio,
    calcular_votos_ponderados,
    verificar_quorum,
)


# def calcular_maioria_simples_assembleia_condominio(valores):
class TestCalcularMaioriaSimplesAssembleiaCondominio:
    def test_numero_par_de_votos(self):
        assert calcular_maioria_simples_assembleia_condominio([1, 1, 1, 1]) == 3

    def test_numero_impar_de_votos(self):
        assert calcular_maioria_simples_assembleia_condominio([1, 1, 1]) == 2

    def test_um_voto(self):
        assert calcular_maioria_simples_assembleia_condominio([1]) == 1


# def calcular_proporcao_ideal_assembleia_condominio(area_unidade, area_total):
class TestCalcularProporcaoIdealAssembleiaCondominio:
    def test_fracao_ideal_basica(self):
        assert calcular_proporcao_ideal_assembleia_condominio(100, 500) == pytest.approx(0.2)

    def test_unidade_igual_area_total(self):
        assert calcular_proporcao_ideal_assembleia_condominio(500, 500) == pytest.approx(1.0)

    def test_unidade_pequena(self):
        assert calcular_proporcao_ideal_assembleia_condominio(50, 1000) == pytest.approx(0.05)

    def test_area_total_zero_lanca_excecao(self):
        with pytest.raises(ValueError):
            calcular_proporcao_ideal_assembleia_condominio(100, 0)

    def test_area_total_negativa_lanca_excecao(self):
        with pytest.raises(ValueError):
            calcular_proporcao_ideal_assembleia_condominio(100, -500)

    def test_area_unidade_negativa_lanca_excecao(self):
        with pytest.raises(ValueError):
            calcular_proporcao_ideal_assembleia_condominio(-100, 500)

# def calcular_votos_ponderados(areas_unidades, votos_unidades):
class TestCalcularVotosPonderados:
    def test_todas_unidades_votando(self):
        areas = [100, 150, 250]
        votos = [1, 1, 1]
        resultado = calcular_votos_ponderados(areas, votos)
        assert resultado == pytest.approx([0.2, 0.3, 0.5])

    def test_unidade_nao_votante(self):
        areas = [100, 150, 250]
        votos = [1, 1, 0]
        resultado = calcular_votos_ponderados(areas, votos)
        assert resultado == pytest.approx([0.2, 0.3, 0.0])

    def test_nenhuma_unidade_votando(self):
        areas = [100, 150, 250]
        votos = [0, 0, 0]
        resultado = calcular_votos_ponderados(areas, votos)
        assert resultado == pytest.approx([0.0, 0.0, 0.0])

#  def calcular_maioria_simples_ponderada(votos_ponderados_favor):
class TestCalcularMaioriaSimplesPonderada:
    def test_maioria_atingida(self):
        assert calcular_maioria_simples_ponderada(0.51) is True

    def test_maioria_nao_atingida(self):
        assert calcular_maioria_simples_ponderada(0.49) is False

    def test_exatamente_metade_maioria(self):
        assert calcular_maioria_simples_ponderada(0.5) is False

# def calcular_maioria_qualificada_ponderada(votos_ponderados_favor, percentual=2/3):
class TestCalcularMaioriaQualificadaPonderada:
    def test_maioria_qualificada_atingida_padrao(self):
        assert calcular_maioria_qualificada_ponderada(2 / 3) is True

    def test_maioria_qualificada_nao_atingida_padrao(self):
        assert calcular_maioria_qualificada_ponderada(0.5) is False

    def test_percentual_customizado(self):
        assert calcular_maioria_qualificada_ponderada(0.75, percentual=0.75) is True
        assert calcular_maioria_qualificada_ponderada(0.74, percentual=0.75) is False


# def apurar_votacao(areas_unidades, votos_unidades, tipo_maioria="simples", metodo_votacao="fracao_ideal"):
class TestApurarVotacao:
    def test_aprovado_por_maioria_simples(self):
        areas = [100, 150, 250]
        votos = [1, 1, -1]  # favor: 250, contra: 250 -> empate, nao aprova
        resultado = apurar_votacao(areas, votos, tipo_maioria="simples")
        assert resultado["aprovado"] is False
        assert resultado["votos_favor"] == pytest.approx(0.5)
        assert resultado["votos_contra"] == pytest.approx(0.5)

    def test_reprovado_por_maioria_simples(self):
        areas = [100, 150, 250]
        votos = [1, -1, -1]  # favor: 100, contra: 400
        resultado = apurar_votacao(areas, votos, tipo_maioria="simples")
        assert resultado["aprovado"] is False
        assert resultado["votos_favor"] == pytest.approx(0.2)
        assert resultado["votos_contra"] == pytest.approx(0.8)

    def test_aprovado_com_abstencoes(self):
        areas = [100, 150, 250]
        votos = [1, 1, 0]  # favor: 250 (50%), abstencao: 250 (50%)
        resultado = apurar_votacao(areas, votos, tipo_maioria="simples")
        assert resultado["aprovado"] is False
        assert resultado["votos_abstencao"] == pytest.approx(0.5)

    def test_maioria_qualificada_aprovada(self):
        areas = [200, 300, 500]
        votos = [1, 1, 1]  # favor: 100%
        resultado = apurar_votacao(areas, votos, tipo_maioria="qualificada")
        assert resultado["aprovado"] is True
        assert resultado["quorum_necessario"] == pytest.approx(2 / 3)

    def test_maioria_qualificada_reprovada(self):
        areas = [200, 300, 500]
        votos = [1, -1, -1]  # favor: 20%
        resultado = apurar_votacao(areas, votos, tipo_maioria="qualificada")
        assert resultado["aprovado"] is False

    def test_tamanhos_diferentes_lanca_excecao(self):
        with pytest.raises(ValueError):
            apurar_votacao([100, 150, 250], [1, -1])

    def test_voto_invalido_lanca_excecao(self):
        with pytest.raises(ValueError):
            apurar_votacao([100, 150], [1, 5])

    def test_lista_vazia_lanca_excecao(self):
        with pytest.raises(ValueError):
            apurar_votacao([], [])

    def test_metodo_unidade_peso_igual_por_unidade(self):
        areas = [50, 100, 1000]
        votos = [1, 1, -1]
        resultado = apurar_votacao(areas, votos, tipo_maioria="simples", metodo_votacao="unidade")
        assert resultado["aprovado"] is True
        assert resultado["votos_favor"] == pytest.approx(2 / 3, abs=1e-4)
        assert resultado["votos_contra"] == pytest.approx(1 / 3, abs=1e-4)
        assert resultado["metodo_votacao"] == "unidade"

    def test_metodo_fracao_ideal_e_o_padrao(self):
        areas = [100, 150, 250]
        votos = [1, 1, -1]
        resultado_padrao = apurar_votacao(areas, votos)
        resultado_explicito = apurar_votacao(areas, votos, metodo_votacao="fracao_ideal")
        assert resultado_padrao == resultado_explicito


# def verificar_quorum(areas_unidades, area_total, convocacao="primeira", quorum_minimo_primeira=2/3, quorum_minimo_segunda=0):
class TestVerificarQuorum:
    def test_primeira_convocacao_quorum_atingido(self):         # presentes: 700 de 1000 (70%) >= 2/3 (~66,67%) 
        resultado = verificar_quorum([300, 400], 1000, convocacao="primeira")
        assert resultado["quorum_atingido"] is True
        assert resultado["fracao_presente"] == pytest.approx(0.7)
        assert resultado["quorum_necessario"] == pytest.approx(2 / 3)

    def test_primeira_convocacao_quorum_nao_atingido(self):
        resultado = verificar_quorum([200, 300], 1000, convocacao="primeira")
        assert resultado["quorum_atingido"] is False

    def test_segunda_convocacao_quorum_atingido(self):          # padrão: quorum_minimo_segunda = 0, então qualquer presença atinge
        resultado = verificar_quorum([50], 1000, convocacao="segunda")
        assert resultado["quorum_atingido"] is True
        assert resultado["fracao_presente"] == pytest.approx(0.05)

    def test_quorum_minimo_customizado(self):
        resultado = verificar_quorum(
            [100], 1000, convocacao="primeira", quorum_minimo_primeira=0.5
        )
        assert resultado["quorum_atingido"] is False
        assert resultado["quorum_necessario"] == pytest.approx(0.5)

    def test_convocacao_invalida_lanca_excecao(self):
        with pytest.raises(ValueError):
            verificar_quorum([100], 1000, convocacao="terceira")

    def test_area_total_zero_lanca_excecao(self):
        with pytest.raises(ValueError):
            verificar_quorum([100], 0)

    def test_area_presente_negativa_lanca_excecao(self):
        with pytest.raises(ValueError):
            verificar_quorum([-100, 200], 1000)
