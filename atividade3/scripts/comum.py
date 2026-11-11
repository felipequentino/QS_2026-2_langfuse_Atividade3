"""Caminhos, versões A/B e utilidades compartilhadas da Atividade 3."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

from app.config import ROOT

AV3 = ROOT / "atividade3"
CASOS = AV3 / "casos" / "casos.yaml"
VERSOES_DIR = AV3 / "versoes"
SAIDAS = AV3 / "saidas"
ANOT = AV3 / "anotacoes"
RES = AV3 / "resultados"

TAU = 0.5          # fixado no plano GQM antes da bateria; não ajustar depois
SEMENTE_CEGA = 20261111
CASOS_R2 = ("CT01", "CT05")

# Única diferença entre as versões: o arquivo de prompt. O resto é a configuração hardened_v2 da AV2.
FLUXO = {"modo_contexto": "auto", "guard": True, "json_mode": True,
         "somente_oficiais": True, "reescrever_consulta": True}
VERSOES = {"A": "P2A", "B": "P2B"}


def registrar_prompts():
    """Faz app.prompts.carregar('P2A'/'P2B') ler os prompts de atividade3/versoes/ (sem alterar app/)."""
    from app import prompts
    for v, pid in VERSOES.items():
        prompts.ARQUIVOS[pid] = str(VERSOES_DIR / v / "prompt.txt")  # Path / absoluto = absoluto


def casos() -> list[dict]:
    return yaml.safe_load(CASOS.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                             check=True).stdout.strip()
        sujo = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
        return sha + ("+alteracoes-nao-commitadas" if sujo else "")
    except Exception:
        return "sem-git"


def ler_saida(versao: str, caso_id: str) -> dict | None:
    p = SAIDAS / versao / f"{caso_id}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def resposta_entregue(saida: dict | None) -> str:
    """Texto que o discente lê: saida_final.resposta. Erro/ausência -> ''."""
    if not saida or saida.get("erro"):
        return ""
    final = saida.get("saida_final") or {}
    return (final.get("resposta") or "").strip()


def ler_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter=";") if any((v or "").strip() for v in r.values())]


def gravar_csv(path: Path, linhas: list[dict], campos: list[str] | None = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    campos = campos or list(linhas[0].keys())
    with open(path, "w", encoding="utf-8-sig", newline="") as f:  # utf-8-sig: abre certo no Excel
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        w.writeheader()
        w.writerows(linhas)
