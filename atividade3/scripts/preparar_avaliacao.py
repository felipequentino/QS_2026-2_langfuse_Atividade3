"""Parte D (preparação): gera as planilhas CEGAS para R1 (12 saídas) e R2 (CT01 e CT05 × A/B = 4 saídas).

Uso: python -m atividade3.scripts.preparar_avaliacao
Saídas em atividade3/anotacoes/:
  planilha_cega_R1.csv   pergunta, referência, trecho, resposta e citações; sem versão e sem F1
  planilha_cega_R2.csv   as 4 linhas revisadas por R2
  chave_cegamento.csv    id_cego -> caso/versão (NÃO abrir antes de terminar as notas)
  R1.csv, R2.csv, consenso.csv   modelos vazios para preencher (nunca sobrescritos se já existirem)
"""
import random

from atividade3.scripts.comum import (ANOT, CASOS_R2, SEMENTE_CEGA, VERSOES, casos, gravar_csv, ler_csv, ler_saida,
                                      resposta_entregue)

CAMPOS_NOTA = ["id_cego", "avaliador", "correcao", "relevancia", "suporte", "falha_critica", "justificativa"]
CAMPOS_CONSENSO = ["id_cego", "correcao", "relevancia", "suporte", "falha_critica", "justificativa_consenso"]


def citacoes(saida: dict | None) -> str:
    final = (saida or {}).get("saida_final") or {}
    return " || ".join(f"[{a.get('doc_id')}] \"{a.get('trecho')}\"" for a in final.get("afirmacoes") or []) or "(nenhuma)"


def main():
    itens = []
    for c in casos():
        for v in VERSOES:
            s = ler_saida(v, c["id"])
            if s is None:
                raise SystemExit(f"Falta a saída {v}/{c['id']}: rode antes python -m atividade3.scripts.executar")
            itens.append((c, v, s))
    random.Random(SEMENTE_CEGA).shuffle(itens)  # semente fixa: ordem reprodutível e sem padrão A/B

    planilha, chave = [], []
    for i, (c, v, s) in enumerate(itens, 1):
        idc = f"S{i:02d}"
        final = s.get("saida_final") or {}
        planilha.append({"id_cego": idc, "pergunta": c["pergunta"], "referencia": c["referencia"],
                         "trecho_fonte": f"[{c['fonte']}] {c['trecho']}", "resposta": resposta_entregue(s) or "(SAÍDA VAZIA OU ERRO)",
                         "recusou": final.get("recusou", ""), "citacoes": citacoes(s)})
        chave.append({"id_cego": idc, "caso_id": c["id"], "versao": v})

    gravar_csv(ANOT / "planilha_cega_R1.csv", planilha)
    ids_r2 = {k["id_cego"] for k in chave if k["caso_id"] in CASOS_R2}
    gravar_csv(ANOT / "planilha_cega_R2.csv", [p for p in planilha if p["id_cego"] in ids_r2])
    gravar_csv(ANOT / "chave_cegamento.csv", chave)

    for nome, ids in (("R1.csv", [p["id_cego"] for p in planilha]), ("R2.csv", sorted(ids_r2))):
        if ler_csv(ANOT / nome) and any(r.get("correcao") for r in ler_csv(ANOT / nome)):
            print(f"{nome} já tem notas: mantido.")
            continue
        gravar_csv(ANOT / nome, [{"id_cego": i, **{k: "" for k in CAMPOS_NOTA[1:]}} for i in ids], CAMPOS_NOTA)
    if not (ANOT / "consenso.csv").exists():
        gravar_csv(ANOT / "consenso.csv", [], CAMPOS_CONSENSO)
    print("Planilhas cegas em atividade3/anotacoes/. R1 preenche R1.csv (12) e R2 preenche R2.csv (4), "
          "sem abrir chave_cegamento.csv nem resultados/.")


if __name__ == "__main__":
    main()
