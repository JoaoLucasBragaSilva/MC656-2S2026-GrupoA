import pytest

from backend.functions.apuracao.proporcional.quociente import (
    calcular_quociente_eleitoral,
    calcular_quociente_partidario,
)

# Testes do quociente eleitoral:

# testa se divisao de votos validos por vagas exata gera a quantidade correta de quociente eleitorial
def test_qe_calculo_exato():
    assert calcular_quociente_eleitoral(1000, 10) == 100

# testa se divisao com fracao exatamente ,5 (nesse caso 100,5) é arredondada para baixo (100)
def test_qe_arredondamento_pra_baixo_exatamente_meio():
    assert calcular_quociente_eleitoral(1005, 10) == 100

# testa se divisao com fracao menor que 0,5 (nesse caso 100,4) é arredondada para baixo (100)
def test_qe_arredondamento_pra_baixo_menor_que_meio():
    assert calcular_quociente_eleitoral(1004, 10) == 100

# testa se divisao com fracao maior que 0,5 (nesse caso 100,6) é arredondada para cima (101)
def test_qe_arredondamento_pra_cima():
    assert calcular_quociente_eleitoral(1006, 10) == 101

# testa se vagas ser zero e se vagas ser valor negativo lança ValueError com a mensagem correta
def test_qe_vagas_menor_igual_a_zero():
    with pytest.raises(ValueError, match="Numero de vagas deve ser maior que zero"):
        calcular_quociente_eleitoral(1000, 0)
        
    with pytest.raises(ValueError, match="Numero de vagas deve ser maior que zero"):
        calcular_quociente_eleitoral(1000, -5)

# testa se votos validos ser menor que zero lança ValueError com a mensagem correta
def test_qe_votos_validos_menor_que_zero():
    with pytest.raises(ValueError, match="Numero de votos validos nao pode ser negativo"):
        calcular_quociente_eleitoral(-10, 12)




# Testes do quociente partidário:

# testa se o valor floor da divisao de votos do partido por QE é retornado como QP
def test_qp_descarte_fracao():
    assert calcular_quociente_partidario(9999, 1000) == 9

# testa se QP é calculado corretamente quando a divisao entre votos do partido e QE é exata
def test_qp_calculo_exato():
    assert calcular_quociente_partidario(1500, 300) == 5

# testa se um valor de votos do partido menor que o de QE gera QP = 0
def test_qp_votos_insuficientes_para_ganhar_vaga():
    assert calcular_quociente_partidario(800, 1000) == 0

# testa se quociente eleitoral ser menor ou igual a zero lança ValueError com a mensagem correta
def test_qp_quociente_eleitoral_menor_igual_a_zero():
    with pytest.raises(ValueError, match="Quociente eleitoral deve ser maior que zero"):
        calcular_quociente_partidario(500, 0)

    with pytest.raises(ValueError, match="Quociente eleitoral deve ser maior que zero"):
        calcular_quociente_partidario(500, -15)

# testa se votos do partido ser menor que zero lança ValueError com a mensagem correta
def test_qp_votos_partido_menor_que_zero():
    with pytest.raises(ValueError, match="Numero de votos do partido nao pode ser negativo"):
        calcular_quociente_partidario(-1, 50)
