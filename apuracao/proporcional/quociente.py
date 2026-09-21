import math


# calcula o quociente eleitoral a partir do numero de votos validos e do numero de vagas
def calcular_quociente_eleitoral(votos_validos: int, vagas: int) -> int:
    if vagas <= 0:
        raise ValueError("Numero de vagas deve ser maior que zero")
    if votos_validos < 0:
        raise ValueError("Numero de votos validos nao pode ser negativo")

    quociente_inteiro, resto = divmod(votos_validos, vagas)

    if resto * 2 > vagas:
        return quociente_inteiro + 1
    else:
        return quociente_inteiro

# calcula o quociente partidario a partir do numero de votos de um partido e do quociente eleitoral
def calcular_quociente_partidario(votos_partido: int, quociente_eleitoral: int) -> int:
    if quociente_eleitoral <= 0:
        raise ValueError("Quociente eleitoral deve ser maior que zero")
    if votos_partido < 0:
        raise ValueError("Numero de votos do partido nao pode ser negativo")

    return votos_partido // quociente_eleitoral
