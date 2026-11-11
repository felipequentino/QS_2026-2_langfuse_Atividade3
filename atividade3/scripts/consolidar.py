"""Partes C e E: F1, sinal automático, decisão humana final, concordâncias, gráfico e decisão experimental.

Uso: python -m atividade3.scripts.consolidar
Lê saidas/, anotacoes/R1.csv, R2.csv, consenso.csv (e IA_adicional.csv, se existir) e grava em resultados/:
  tabela_12.csv   uma linha por saída (caso/versão, F1, sinal automático, notas, decisão final, justificativa)
  resumo.json     números por versão e concordâncias, com denominadores explícitos
  resultados.md   tabela consolidada + interpretação mecânica (incluída no relatório)
  grafico.png     visualização simples
Funciona com dados parciais: o que falta aparece como "pendente", nunca como número inventado.
"""
import json
import statistics

from atividade3.scripts.comum import (ANOT, CASOS_R2, RES, TAU, VERSOES, casos, gravar_csv, ler_csv, ler_saida,
                                      resposta_entregue)
from atividade3.scripts.f1 import f1_lexical

DIMS = ("correcao", "relevancia", "suporte")


def nota(linha: dict | None) -> dict | None:
    """Converte uma linha de anotação em notas inteiras; None se incompleta. Valores fora da escala abortam."""
    if not linha or not all((linha.get(k) or "").strip() for k in DIMS + ("falha_critica",)):
        return None
    n = {k: int(linha[k]) for k in DIMS + ("falha_critica",)}
    if any(n[k] not in (0, 1, 2) for k in DIMS) or n["falha_critica"] not in (0, 1):
        raise SystemExit(f"nota fora da escala em {linha}")
    n["aprovado"] = all(n[k] == 2 for k in DIMS) and n["falha_critica"] == 0
    n["justificativa"] = (linha.get("justificativa") or linha.get("justificativa_consenso") or "").strip()
    return n


def fmt_notas(n: dict | None) -> str:
    return "pendente" if n is None else f"C{n['correcao']} R{n['relevancia']} S{n['suporte']} FC{n['falha_critica']}"


def decidir(res: dict) -> tuple[str, str]:
    """Critério pré-registrado em plano_gqm.md."""
    a, b = res["por_versao"]["A"], res["por_versao"]["B"]
    if a["aprovacao_humana"] is None or b["aprovacao_humana"] is None:
        return "pendente", "faltam decisões humanas finais"
    if b["falhas_criticas"] > 0:
        return "revisar B", f"bloqueio: B tem {b['falhas_criticas']} falha(s) crítica(s); A permanece em uso"
    if b["aprovados"] > a["aprovados"]:
        return "levar B à próxima etapa", f"aprovação humana B {b['aprovados']}/6 > A {a['aprovados']}/6, sem falha crítica"
    return "manter A", f"aprovação humana B {b['aprovados']}/6 ≤ A {a['aprovados']}/6 (ganho só de F1 não conta)"


def grafico(linhas: list[dict], res: dict):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cor = {"A": "#2a78d6", "B": "#eb6834"}  # slots 1 e 2 da paleta categórica validada (skill dataviz)
    tinta, tinta2, grade = "#0b0b0b", "#52514e", "#e4e3df"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": grade, "axes.labelcolor": tinta2,
                         "xtick.color": tinta2, "ytick.color": tinta2})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [2.3, 1]})
    ids = [c["id"] for c in casos()]
    w = 0.38
    for j, v in enumerate(VERSOES):
        for i, cid in enumerate(ids):
            l = next(x for x in linhas if x["caso_id"] == cid and x["versao"] == v)
            if l["f1"] == "":
                continue
            x = i + (j - 0.5) * w
            ax1.bar(x, float(l["f1"]), w * 0.92, color=cor[v], label=f"Versão {v}" if i == 0 else None)
            marca = {"sim": "✓", "não": "✗"}.get(l["aprovacao_humana_final"], "?")
            ax1.text(x, float(l["f1"]) + 0.02, marca, ha="center", va="bottom", color=tinta, fontsize=10)
    ax1.axhline(TAU, color=tinta2, lw=1, ls="--")
    ax1.text(1.005, TAU, f"τ = {TAU}", transform=ax1.get_yaxis_transform(), ha="left", va="center", color=tinta2)
    ax1.set_xticks(range(len(ids)), ids)
    ax1.set_ylim(0, 1.12)
    ax1.set_ylabel("F1 lexical")
    ax1.set_title("F1 por caso  (✓/✗ = decisão humana final)", loc="left", color=tinta, fontsize=10)
    ax1.legend(frameon=False, loc="upper left", ncol=2)

    medidas = [("aprovados", "Aprovação humana"), ("auto_aprovados", "Sinal automático (F1 ≥ τ)")]
    for j, v in enumerate(VERSOES):
        for k, (campo, rotulo) in enumerate(medidas):
            val = res["por_versao"][v][campo]
            if val is None:
                continue
            x = k + (j - 0.5) * w
            ax2.bar(x, val, w * 0.92, color=cor[v], hatch="///" if k else None, edgecolor="white", lw=0)
            ax2.text(x, val + 0.08, f"{val}/6", ha="center", va="bottom", color=tinta, fontsize=9)
    ax2.set_xticks(range(len(medidas)), [m[1].replace(" (", "\n(") for m in medidas])
    ax2.set_ylim(0, 6.8)
    ax2.set_yticks(range(0, 7))
    ax2.set_title("Saídas aprovadas por versão (de 6)", loc="left", color=tinta, fontsize=10)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color=grade, lw=0.6)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(RES / "grafico.png", dpi=180)
    plt.close(fig)


def main():
    chave = {k["id_cego"]: k for k in ler_csv(ANOT / "chave_cegamento.csv")}
    por_caso = {(k["caso_id"], k["versao"]): idc for idc, k in chave.items()}
    r1 = {l["id_cego"]: l for l in ler_csv(ANOT / "R1.csv")}
    r2 = {l["id_cego"]: l for l in ler_csv(ANOT / "R2.csv")}
    cons = {l["id_cego"]: l for l in ler_csv(ANOT / "consenso.csv")}
    ia = {l["id_cego"]: l for l in ler_csv(ANOT / "IA_adicional.csv")}

    linhas, revisadas = [], []
    for c in casos():
        for v in VERSOES:
            s = ler_saida(v, c["id"])
            idc = por_caso.get((c["id"], v), "")
            n1, n2, nc = nota(r1.get(idc)), nota(r2.get(idc)), nota(cons.get(idc))
            final = nc or n1
            origem = "consenso R1–R2" if nc else ("R1" if n1 else "")
            f = f1_lexical(resposta_entregue(s), c["referencia"]) if s is not None else None
            auto = None if f is None else f["f1"] >= TAU
            if c["id"] in CASOS_R2:
                revisadas.append({"caso_id": c["id"], "versao": v, "id_cego": idc, "r1": n1, "r2": n2, "consenso": nc})
            ni = nota(ia.get(idc))
            linhas.append({
                "caso_id": c["id"], "versao": v, "tipo": c["tipo"], "id_cego": idc,
                "status_saida": "pendente" if s is None else ("erro" if s.get("erro") else "ok"),
                "resposta": resposta_entregue(s), "f1": "" if f is None else f"{f['f1']:.3f}",
                "p_tokens": "" if f is None else f["p"], "r_tokens": "" if f is None else f["r"],
                "sinal_automatico": "" if auto is None else ("aprova" if auto else "reprova"),
                "notas_R1": fmt_notas(n1), "notas_R2": fmt_notas(n2) if c["id"] in CASOS_R2 else "—",
                "notas_consenso": fmt_notas(nc) if nc else "—", "origem_decisao": origem,
                "aprovacao_humana_final": "" if final is None else ("sim" if final["aprovado"] else "não"),
                "falha_critica_final": "" if final is None else final["falha_critica"],
                "justificativa": "" if final is None else final["justificativa"],
                "concorda_auto_humano": "" if (final is None or auto is None) else ("sim" if auto == final["aprovado"] else "não"),
                "IA_adicional_aprova": "" if ni is None else ("sim" if ni["aprovado"] else "não"),
                "trace_url": (s or {}).get("trace_url") or "",
            })

    res = {"tau": TAU, "por_versao": {}, "status": {
        "saidas": sum(l["status_saida"] != "pendente" for l in linhas),
        "saidas_com_erro": sum(l["status_saida"] == "erro" for l in linhas),
        "anotacoes_R1": sum(nota(x) is not None for x in r1.values()),
        "anotacoes_R2": sum(nota(x) is not None for x in r2.values()),
        "consensos": sum(nota(x) is not None for x in cons.values())}}
    for v in VERSOES:
        lv = [l for l in linhas if l["versao"] == v]
        f1s = [float(l["f1"]) for l in lv if l["f1"] != ""]
        hum = [l for l in lv if l["aprovacao_humana_final"] != ""]
        completo_f1, completo_h = len(f1s) == 6, len(hum) == 6
        res["por_versao"][v] = {
            "f1_medio": round(statistics.mean(f1s), 3) if completo_f1 else None,
            "f1_mediano": round(statistics.median(f1s), 3) if completo_f1 else None,
            "auto_aprovados": sum(l["sinal_automatico"] == "aprova" for l in lv) if completo_f1 else None,
            "aprovados": sum(l["aprovacao_humana_final"] == "sim" for l in hum) if completo_h else None,
            "aprovacao_humana": round(sum(l["aprovacao_humana_final"] == "sim" for l in hum) / 6, 3) if completo_h else None,
            "falhas_criticas": sum(int(l["falha_critica_final"]) for l in hum) if completo_h else None,
            "denominador": 6}
    pares = [l for l in linhas if l["concorda_auto_humano"] != ""]
    res["concordancia_auto_humano"] = ({"iguais": sum(l["concorda_auto_humano"] == "sim" for l in pares), "denominador": 12}
                                       if len(pares) == 12 else None)
    comp = [x for x in revisadas if x["r1"] and x["r2"]]
    res["concordancia_R1_R2"] = ({"iguais": sum(x["r1"]["aprovado"] == x["r2"]["aprovado"] for x in comp),
                                  "notas_identicas": sum(all(x["r1"][k] == x["r2"][k] for k in DIMS + ("falha_critica",)) for x in comp),
                                  "denominador": 4, "momento": "antes do consenso"} if len(comp) == 4 else None)
    res["divergencias_sem_consenso"] = [x["id_cego"] for x in comp
                                        if (x["r1"]["aprovado"] != x["r2"]["aprovado"]
                                            or x["r1"]["falha_critica"] != x["r2"]["falha_critica"]) and not x["consenso"]]
    pares_ia = [l for l in linhas if l["IA_adicional_aprova"] and l["aprovacao_humana_final"]]
    res["concordancia_IA_humano"] = ({"iguais": sum(l["IA_adicional_aprova"] == l["aprovacao_humana_final"] for l in pares_ia),
                                      "denominador": len(pares_ia)} if pares_ia else None)
    res["decisao"], res["motivo_decisao"] = decidir(res)
    if res["decisao"] != "pendente" and res["concordancia_R1_R2"] is None:
        res["decisao"] += " (provisória)"
        res["motivo_decisao"] += "; R2 ainda não avaliou CT01/CT05, e um consenso pode alterar essas 4 decisões"
    if res["divergencias_sem_consenso"]:
        res["decisao"], res["motivo_decisao"] = "pendente", "divergência R1–R2 sem consenso registrado"
    res["divergencias_auto_humano"] = [f"{l['caso_id']}/{l['versao']}" for l in linhas if l["concorda_auto_humano"] == "não"]

    RES.mkdir(parents=True, exist_ok=True)
    gravar_csv(RES / "tabela_12.csv", linhas)
    (RES / "resumo.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    if res["status"]["saidas"]:
        grafico(linhas, res)
    (RES / "resultados.md").write_text(markdown(linhas, res, revisadas), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("status", "por_versao", "concordancia_auto_humano", "concordancia_R1_R2",
                                          "decisao", "motivo_decisao")}, ensure_ascii=False, indent=1))


def _n(x, suf=""):
    return "pendente" if x is None else f"{x}{suf}"


def markdown(linhas, res, revisadas) -> str:
    st = res["status"]
    out = ["# Resultados consolidados", "",
           f"Gerado por `python -m atividade3.scripts.consolidar`. Estado: **{st['saidas']}/12 saídas** "
           f"({st['saidas_com_erro']} com erro), **{st['anotacoes_R1']}/12 notas R1**, **{st['anotacoes_R2']}/4 notas R2**, "
           f"{st['consensos']} consenso(s). τ = {res['tau']}.", ""]
    if st["saidas"] < 12 or st["anotacoes_R1"] < 12 or st["anotacoes_R2"] < 4:
        out += ["> **Execução/avaliação incompleta.** Campos sem dado aparecem como *pendente*; nenhum número foi "
                "estimado ou inventado.", ""]
    out += ["## Tabela das 12 saídas", "",
            "| Caso | Versão | F1 | Sinal auto | Notas R1 | Notas R2 | Consenso | Decisão humana final | Auto = humano? | Justificativa |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for l in linhas:
        out.append(f"| {l['caso_id']} | {l['versao']} | {l['f1'] or 'pendente'} | {l['sinal_automatico'] or 'pendente'} | "
                   f"{l['notas_R1']} | {l['notas_R2']} | {l['notas_consenso']} | "
                   f"{(l['aprovacao_humana_final'] + ' (' + l['origem_decisao'] + ')') if l['aprovacao_humana_final'] else 'pendente'} | "
                   f"{l['concorda_auto_humano'] or 'pendente'} | {l['justificativa'].replace('|', '/') or '—'} |")
    out += ["", "Notas: C = correção, R = relevância, S = suporte (0–2), FC = falha crítica (0/1). "
            "Aprovação humana = C2 R2 S2 e FC0.", "", "## Resumo por versão (denominador 6)", "",
            "| Medida | Versão A | Versão B |", "|---|---|---|"]
    a, b = res["por_versao"]["A"], res["por_versao"]["B"]
    out += [f"| F1 médio | {_n(a['f1_medio'])} | {_n(b['f1_medio'])} |",
            f"| F1 mediano | {_n(a['f1_mediano'])} | {_n(b['f1_mediano'])} |",
            f"| Sinal automático aprova (F1 ≥ τ) | {_n(a['auto_aprovados'], '/6')} | {_n(b['auto_aprovados'], '/6')} |",
            f"| **Aprovação humana** | {_n(a['aprovados'], '/6')} | {_n(b['aprovados'], '/6')} |",
            f"| Falhas críticas | {_n(a['falhas_criticas'], '/6')} | {_n(b['falhas_criticas'], '/6')} |", ""]
    cah, crr = res["concordancia_auto_humano"], res["concordancia_R1_R2"]
    out += ["## Concordâncias", "",
            f"- **Auto–humano** (sinal F1 ≥ τ × decisão humana final): "
            f"{'pendente' if cah is None else str(cah['iguais']) + '/12'}.",
            f"- **R1–R2** (decisão aprovado/reprovado, só nas 4 saídas revisadas, antes do consenso): "
            f"{'pendente' if crr is None else str(crr['iguais']) + '/4'}"
            f"{'' if crr is None else '; notas idênticas nas 4 dimensões em ' + str(crr['notas_identicas']) + '/4'}.",
            ]
    if res["concordancia_IA_humano"]:
        ci = res["concordancia_IA_humano"]
        out.append(f"- *Avaliação adicional por LLM (não humana, não entra na decisão)* × decisão humana: "
                   f"{ci['iguais']}/{ci['denominador']}.")
    out += ["", "### Saídas revisadas por R2", "", "| Caso | Versão | R1 | R2 | Consenso |", "|---|---|---|---|---|"]
    for x in revisadas:
        out.append(f"| {x['caso_id']} | {x['versao']} | {fmt_notas(x['r1'])} | {fmt_notas(x['r2'])} | "
                   f"{fmt_notas(x['consenso']) if x['consenso'] else '—'} |")
    out += ["", "## Divergências automático × humano", ""]
    if cah is None:
        out.append("Pendente (faltam saídas ou decisões humanas).")
    elif res["divergencias_auto_humano"]:
        out.append("Saídas em que o sinal automático e a decisão humana discordam: " +
                   ", ".join(res["divergencias_auto_humano"]) + ". A análise qualitativa está em "
                   "`docs/analise_divergencia.md`.")
    else:
        out.append("Nenhuma divergência nas 12 decisões; o caso-limite discutido está em `docs/analise_divergencia.md`.")
    out += ["", "## Decisão experimental (critério pré-registrado)", "",
            f"**{res['decisao']}** — {res['motivo_decisao']}. Não é autorização para produção.", ""]
    if st["saidas"]:
        out += ["![Gráfico](grafico.png)", ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
