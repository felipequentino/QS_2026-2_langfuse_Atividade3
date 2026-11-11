"""Apoio à escolha de τ (antes da bateria): F1 de saídas REAIS já existentes da AV2 contra as referências da AV3.

Uso: python -m atividade3.scripts.calibracao_tau <caminho para run_tests_*.jsonl da AV2>
Grava atividade3/resultados/calibracao_tau.md. Não usa nenhuma saída da AV3.
"""
import json
import sys
from pathlib import Path

from atividade3.scripts.comum import RES, TAU, casos
from atividade3.scripts.f1 import f1_lexical

# (caso AV2, variante AV2, caso AV3 cuja referência é comparável, julgamento humano declarado da saída da AV2)
PARES = [("CT-CTX-01", "hardened_v2", "CT01", "correta mas incompleta (omite frequência de 75%)"),
         ("CT-FUN-02", "hardened_v2", "CT03", "correta para a pergunta da AV2 (só prazo)"),
         ("CT-INJ-03", "hardened_v2", "CT02", "correta e completa"),
         ("CT-CTX-03", "hardened_v2", "CT05", "abstenção correta (contexto irrelevante na AV2)")]


def main(log: Path):
    refs = {c["id"]: c["referencia"] for c in casos()}
    saidas = {}
    for linha in log.open(encoding="utf-8"):
        r = json.loads(linha)
        res = r["resultado"][0] if isinstance(r["resultado"], list) else r["resultado"]
        if res.get("saida_final"):  # baseline (P1) não tem saida_final estruturada
            saidas.setdefault((r["caso_id"], r["variante"]), res["saida_final"]["resposta"])
    linhas = ["| Saída real da AV2 | Referência AV3 | Resposta (resumo) | F1 | F1 ≥ τ? | Leitura qualitativa (apoio ao τ) |",
              "|---|---|---|---|---|---|"]
    for c2, v, c3, leitura in PARES:
        resp = saidas[(c2, v)]
        f = f1_lexical(resp, refs[c3])
        linhas.append(f"| {c2} ({v}) | {c3} | {resp[:90]}{'…' if len(resp) > 90 else ''} | {f['f1']:.3f} | "
                      f"{'sim' if f['f1'] >= TAU else 'não'} | {leitura} |")
    out = RES / "calibracao_tau.md"
    RES.mkdir(parents=True, exist_ok=True)
    out.write_text(f"Fonte: `{log.name}` (AV2, 21/10/2026). τ = {TAU}.\n\n" + "\n".join(linhas) + "\n",
                   encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
