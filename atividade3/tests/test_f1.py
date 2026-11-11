"""Testes offline da métrica F1 lexical (sem chave de API)."""
import pytest

from atividade3.scripts.f1 import f1_lexical, tokens


def test_tokenizacao_nfc_casefold():
    # "é" decomposto (e + acento combinante) e composto viram o mesmo token
    assert tokens("É Média 7,0") == tokens("é MÉDIA 7,0") == ["é", "média", "7", "0"]


def test_identico_vale_1():
    assert f1_lexical("Até 5 dias úteis.", "até 5 dias úteis")["f1"] == 1.0


def test_calculo_a_mao():
    # resp: a b b c (4) | ref: a b d (3) | comuns multiconjunto: a, b = 2 -> P=0,5 R=0,667 F1=0,571
    r = f1_lexical("a b b c", "a b d")
    assert (r["comuns"], r["p"], r["r"], r["f1"]) == (2, 0.5, 0.667, 0.571)


def test_vazio_e_sem_sobreposicao_valem_0():
    assert f1_lexical("", "prazo de 5 dias")["f1"] == 0.0
    assert f1_lexical("xyz", "prazo de 5 dias")["f1"] == 0.0


def test_referencia_vazia_e_erro():
    with pytest.raises(ValueError):
        f1_lexical("qualquer", "  ,. ")


def test_limite_conhecido_troca_de_numero():
    # trocar 7,0 por 6,0 muda a resposta factual mas mantém F1 alto
    ref = "média igual ou superior a 7,0"
    assert f1_lexical("média igual ou superior a 6,0", ref)["f1"] >= 0.8
