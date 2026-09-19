import math             #Assembleia condominio
import numpy as np

def calcular_maioria_simples_assembleia_condominio(valores):
    total_votos = sum(valores)
    votos_necessarios = math.floor(total_votos / 2) + 1
    return votos_necessarios

def calcular_proporcao_ideal_assembleia_condominio(area_unidade, area_total):

    if area_total <= 0:
        raise ValueError("area_total deve ser maior que 0")
    if area_unidade < 0:
        raise ValueError("area_unidade deve ser maior que 0")

    fracao_ideal = area_unidade / area_total
    return fracao_ideal


def calcular_votos_ponderados(areas_unidades, votos_unidades):  # Calcula os votos ponderados de todas as unidades

    area_total = sum(areas_unidades)    # Calcula a área total das unidades
    votos_ponderados = []               # Um array para armazenar os votos ponderados de cada unidade

    for area, voto in zip(areas_unidades, votos_unidades):
        fracao = calcular_proporcao_ideal_assembleia_condominio(area, area_total)
        peso_voto = fracao * np.abs(voto)       # Multiplica pela presença do voto (0 ou 1)
        votos_ponderados.append(peso_voto)

    return votos_ponderados             # Lista com os pesos dos votos ponderados de cada unidade

def calcular_maioria_simples_ponderada(votos_ponderados_favor):
    return votos_ponderados_favor > 0.5

def calcular_maioria_qualificada_ponderada(votos_ponderados_favor, percentual=2/3):
    return votos_ponderados_favor >= percentual


def verificar_quorum(areas_presentes, area_total, convocacao="primeira", quorum_minimo_primeira=2/3, quorum_minimo_segunda=0.0):
    if convocacao not in ("primeira", "segunda"):
        raise ValueError("convocacao deve ser 'primeira' ou 'segunda'")
    if area_total <= 0:
        raise ValueError("area_total deve ser maior que 0")
    if any(area < 0 for area in areas_presentes):
        raise ValueError("areas_presentes deve conter apenas valores maiores ou iguais a 0")
    fracao_presente = sum(areas_presentes) / area_total
    if convocacao == "primeira":
        quorum_necessario = quorum_minimo_primeira
    else:
        quorum_necessario = quorum_minimo_segunda
    quorum_atingido = fracao_presente >= quorum_necessario

    return {
        "quorum_atingido": quorum_atingido,
        "fracao_presente": round(fracao_presente, 2),
        "percentual_presente": round(fracao_presente * 100, 2),
        "quorum_necessario": quorum_necessario,
        "convocacao": convocacao,
    }

def apurar_votacao(areas_unidades, votos_unidades, tipo_maioria="simples", metodo_votacao="fracao_ideal"):

    if len(areas_unidades) != len(votos_unidades):
        raise ValueError("areas_unidades e votos_unidades devem ter o mesmo tamanho")
    if any(voto not in (0, 1, -1) for voto in votos_unidades):
        raise ValueError("votos_unidades deve conter apenas 0, 1 ou -1")
    if metodo_votacao not in ("fracao_ideal", "unidade"):
        raise ValueError("metodo_votacao deve ser 'fracao_ideal' ou 'unidade'")
    if tipo_maioria not in ("simples", "qualificada"):
        raise ValueError("tipo_maioria deve ser 'simples' ou 'qualificada'")
    if len(areas_unidades) == 0:
        raise ValueError("areas_unidades não pode estar vazio")

    if metodo_votacao == "fracao_ideal":
        area_total = sum(areas_unidades)
        pesos = [calcular_proporcao_ideal_assembleia_condominio(area, area_total) for area in areas_unidades]
    else:       # metodo_votacao == "unidade"
        peso_unitario = 1 / len(areas_unidades)
        pesos = [peso_unitario] * len(areas_unidades)

    votos_favor = 0
    votos_contra = 0
    votos_abstencao = 0

    for peso, voto in zip(pesos, votos_unidades):
        if voto == 1:
            votos_favor += peso
        elif voto == -1:
            votos_contra += peso
        else:
            votos_abstencao += peso
    if tipo_maioria == "simples":
        resultado = calcular_maioria_simples_ponderada(votos_favor)
        quorum_necessario = 0.5
    else:
        resultado = calcular_maioria_qualificada_ponderada(votos_favor)
        quorum_necessario = 2 / 3

    return {
        "aprovado": resultado,
        "votos_favor": round(votos_favor, 4),
        "votos_contra": round(votos_contra, 4),
        "votos_abstencao": round(votos_abstencao, 4),
        "percentual_favor": round(votos_favor * 100, 2),
        "percentual_contra": round(votos_contra * 100, 2),
        "percentual_abstencao": round(votos_abstencao * 100, 2),
        "quorum_necessario": quorum_necessario,
        "tipo_maioria": tipo_maioria,
        "metodo_votacao": metodo_votacao,
    }