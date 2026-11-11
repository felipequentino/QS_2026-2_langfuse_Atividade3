"""Métrica automática da Parte C: F1 lexical por tokens (NFC, casefold, tokens de palavra, multiconjunto).

    P_tokens = comuns / tokens_da_resposta
    R_tokens = comuns / tokens_da_referencia
    F1       = 2 * P * R / (P + R)      sem sobreposição ou resposta vazia -> 0
Referência sem tokens é erro do caso (ValueError), nunca um score inventado.
"""
import re
import unicodedata
from collections import Counter

_PALAVRA = re.compile(r"\w+")


def tokens(texto: str) -> list[str]:
    return _PALAVRA.findall(unicodedata.normalize("NFC", texto or "").casefold())


def f1_lexical(resposta: str, referencia: str) -> dict:
    ref, resp = Counter(tokens(referencia)), Counter(tokens(resposta))
    if not ref:
        raise ValueError("referência sem tokens: corrigir o caso")
    comuns = sum((ref & resp).values())
    n_resp, n_ref = sum(resp.values()), sum(ref.values())
    if comuns == 0 or n_resp == 0:
        return {"p": 0.0, "r": 0.0, "f1": 0.0, "comuns": comuns, "n_resp": n_resp, "n_ref": n_ref}
    p, r = comuns / n_resp, comuns / n_ref
    return {"p": round(p, 3), "r": round(r, 3), "f1": round(2 * p * r / (p + r), 3),
            "comuns": comuns, "n_resp": n_resp, "n_ref": n_ref}
