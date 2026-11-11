"""Gera relatorio/relatorio.pdf e apresentacao/slides.pdf a partir dos artefatos e de resultados/resumo.json.

Markdown -> HTML com a biblioteca `markdown` (sem Pandoc) -> PDF com Chrome/Chromium headless.
Rodar depois de consolidar.py:  python -m atividade3.scripts.build_pdfs
Adaptado de scripts/build_pdfs.py da AV2.
"""
import base64
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

import markdown
import yaml

from atividade3.scripts.comum import AV3, RES

NAVEGADORES = ["google-chrome", "chromium", "chromium-browser", "msedge",
               r"C:\Program Files\Google\Chrome\Application\chrome.exe",
               r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
MERMAID = ('<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>'
           '<script>mermaid.initialize({startOnLoad:true, theme:"neutral", flowchart:{useMaxWidth:true}});</script>')
INCLUDE = re.compile(r"\{\{include ([^}]+)\}\}")


def navegador() -> str:
    for n in NAVEGADORES:
        if shutil.which(n) or Path(n).exists():
            return n
    raise SystemExit("Chrome/Chromium/Edge não encontrado")


def imprimir(html_path: Path, pdf: Path):
    subprocess.run([navegador(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", html_path.as_uri()],
                   check=True, capture_output=True)
    print("gerado:", pdf.relative_to(AV3.parent))


def resumo() -> dict:
    p = RES / "resumo.json"
    if not p.exists():
        raise SystemExit("Rode antes: python -m atividade3.scripts.consolidar")
    return json.loads(p.read_text(encoding="utf-8"))


def frase_melhoria(r: dict) -> str:
    a, b = r["por_versao"]["A"], r["por_versao"]["B"]
    if a["aprovados"] is None or b["aprovados"] is None or a["f1_medio"] is None:
        return "pendente (faltam saídas ou decisões humanas)."
    dh = b["aprovados"] - a["aprovados"]
    df = round(b["f1_medio"] - a["f1_medio"], 3)
    humano = "melhorou" if dh > 0 else ("piorou" if dh < 0 else "não mudou")
    auto = "subiu" if df > 0 else ("caiu" if df < 0 else "não mudou")
    return (f"Aprovação humana {a['aprovados']}/6 → {b['aprovados']}/6 ({humano}); F1 médio {a['f1_medio']} → "
            f"{b['f1_medio']} ({auto}). Falhas críticas: A {a['falhas_criticas']}, B {b['falhas_criticas']}.")


def substituir(texto: str, r: dict, links: dict) -> str:
    valores = {"repo_url": links.get("repo_url") or "(a definir)",
               "video_url": links.get("video_url") or "(a preencher em VIDEO.md)",
               "decisao": f"**{r['decisao']}** — {r['motivo_decisao']}.",
               "q_melhoria": frase_melhoria(r)}
    return re.sub(r"\{\{(\w+)\}\}", lambda m: valores.get(m.group(1), m.group(0)), texto)


def expandir_includes(fonte: Path) -> str:
    """Insere cada arquivo rebaixando títulos (# -> ###) e corrigindo caminhos de imagens relativas."""
    def inserir(m):
        alvo = (fonte.parent / m.group(1)).resolve()
        texto = alvo.read_text(encoding="utf-8")
        texto = re.sub(r"^(#{1,4}) ", lambda h: "#" * min(len(h.group(1)) + 2, 6) + " ", texto, flags=re.M)
        base = Path(m.group(1)).parent.as_posix()
        return re.sub(r"!\[([^\]]*)\]\((?!https?:)([^)]+)\)", lambda i: f"![{i.group(1)}]({base}/{i.group(2)})", texto)
    return INCLUDE.sub(inserir, fonte.read_text(encoding="utf-8"))


def relatorio(r: dict, links: dict):
    pasta = AV3 / "relatorio"
    md = substituir(expandir_includes(pasta / "relatorio_fonte.md"), r, links)
    (pasta / "relatorio.md").write_text("<!-- gerado por build_pdfs.py a partir de relatorio_fonte.md; não editar -->\n"
                                        + md, encoding="utf-8")
    corpo = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
    corpo = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>',
                   lambda m: f'<pre class="mermaid">{m.group(1)}</pre>', corpo, flags=re.S)
    doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Relatório AV3</title>'
           f'<link rel="stylesheet" href="estilo.css"></head><body>{corpo}{MERMAID}</body></html>')
    h = pasta / "relatorio.html"
    h.write_text(doc, encoding="utf-8")
    imprimir(h, pasta / "relatorio.pdf")


def slides(r: dict, links: dict):
    pasta = AV3 / "apresentacao"
    t = (pasta / "slides_fonte.html").read_text(encoding="utf-8")
    a, b = r["por_versao"]["A"], r["por_versao"]["B"]
    n = lambda x, s="": "pendente" if x is None else f"{x}{s}"  # noqa: E731
    cah, crr = r["concordancia_auto_humano"], r["concordancia_R1_R2"]
    graf = RES / "grafico.png"
    img = (f'<img src="data:image/png;base64,{base64.b64encode(graf.read_bytes()).decode()}" alt="Gráfico F1 e aprovação">'
           if graf.exists() else '<p class="pend">Gráfico pendente: execute a bateria e consolide.</p>')
    linhas = []
    import csv
    with open(RES / "tabela_12.csv", encoding="utf-8-sig") as f:
        for l in csv.DictReader(f, delimiter=";"):
            linhas.append(f"<tr><td>{l['caso_id']}</td><td>{l['versao']}</td><td>{l['f1'] or '—'}</td>"
                          f"<td>{l['sinal_automatico'] or '—'}</td><td>{l['notas_R1']}</td>"
                          f"<td>{l['aprovacao_humana_final'] or '—'}</td><td>{l['concorda_auto_humano'] or '—'}</td></tr>")
    valores = {
        "F1_A": n(a["f1_medio"]), "F1_B": n(b["f1_medio"]), "F1MED_A": n(a["f1_mediano"]), "F1MED_B": n(b["f1_mediano"]),
        "AUTO_A": n(a["auto_aprovados"], "/6"), "AUTO_B": n(b["auto_aprovados"], "/6"),
        "HUM_A": n(a["aprovados"], "/6"), "HUM_B": n(b["aprovados"], "/6"),
        "FC_A": n(a["falhas_criticas"]), "FC_B": n(b["falhas_criticas"]),
        "CONC_AH": "pendente" if cah is None else f"{cah['iguais']}/12",
        "CONC_RR": "pendente" if crr is None else f"{crr['iguais']}/4",
        "DECISAO": html.escape(r["decisao"]), "MOTIVO": html.escape(r["motivo_decisao"]),
        "DIVERG": html.escape(", ".join(r["divergencias_auto_humano"]) or "nenhuma / pendente"),
        "STATUS": f"{r['status']['saidas']}/12 saídas · {r['status']['anotacoes_R1']}/12 R1 · {r['status']['anotacoes_R2']}/4 R2",
        "GRAFICO": img, "TABELA": "\n".join(linhas),
        "REPO": html.escape(links.get("repo_url") or "(a definir)"),
        "VIDEO": html.escape(links.get("video_url") or "(link em VIDEO.md)"),
    }
    t = re.sub(r"\{\{(\w+)\}\}", lambda m: valores.get(m.group(1), m.group(0)), t)
    h = pasta / "slides.html"
    h.write_text(t, encoding="utf-8")
    imprimir(h, pasta / "slides.pdf")


if __name__ == "__main__":
    res, lk = resumo(), yaml.safe_load((AV3 / "links.yaml").read_text(encoding="utf-8")) or {}
    relatorio(res, lk)
    slides(res, lk)
