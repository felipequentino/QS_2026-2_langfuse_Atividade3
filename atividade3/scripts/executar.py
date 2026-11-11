"""Parte B: executa cada caso UMA vez em A e UMA vez em B e guarda as 12 saídas brutas.

Uso (na raiz do repositório, com .env preenchido):
    python -m atividade3.scripts.executar              # A e B, CT01..CT06
    python -m atividade3.scripts.executar --versao B   # só B (ex.: se A já foi executada)

Regras do enunciado aplicadas aqui:
- nunca sobrescreve uma saída existente (para refazer, mova a pasta e registre o motivo no README);
- falha de chamada vira saída registrada com "erro" (não é descartada nem refeita em silêncio);
- cada arquivo guarda versão, caso, configuração, prompt (sha256), modelo e o contexto efetivamente usado.
"""
import argparse
import json
import platform
import traceback
from datetime import datetime, timezone

from app import config
from atividade3.scripts.comum import (FLUXO, SAIDAS, VERSOES, VERSOES_DIR, casos, git_commit,
                                      registrar_prompts, sha256)


def executar_versao(versao: str, sessao: str) -> dict:
    from app.pipeline import responder  # import tardio: só depois de registrar os prompts
    pid, pasta = VERSOES[versao], SAIDAS / versao
    pasta.mkdir(parents=True, exist_ok=True)
    prompt_path = VERSOES_DIR / versao / "prompt.txt"
    registro = {"versao": versao, "prompt_id": pid, "prompt_arquivo": str(prompt_path.relative_to(config.ROOT)),
                "prompt_sha256": sha256(prompt_path), "commit": git_commit(),
                "provedor": config.PROVIDER, "modelo": config.MODEL, "temperatura": config.TEMPERATURE,
                "top_k": config.TOP_K, "fluxo": FLUXO, "sessao_langfuse": sessao,
                "python": platform.python_version(), "inicio_utc": datetime.now(timezone.utc).isoformat(),
                "saidas": []}
    for caso in casos():
        destino = pasta / f"{caso['id']}.json"
        if destino.exists():
            raise SystemExit(f"{destino} já existe: não sobrescrevo saídas brutas.")
        base = {"versao": versao, "caso_id": caso["id"], "tipo": caso["tipo"], "pergunta": caso["pergunta"],
                "configuracao": {"prompt_id": pid, "prompt_sha256": registro["prompt_sha256"], **FLUXO,
                                 "provedor": config.PROVIDER, "modelo": config.MODEL,
                                 "temperatura": config.TEMPERATURE, "top_k": config.TOP_K},
                "executado_em_utc": datetime.now(timezone.utc).isoformat(), "commit": registro["commit"]}
        try:
            r = responder(caso["pergunta"], prompt_id=pid, rotulo=f"av3-{versao}-{caso['id']}", sessao=sessao,
                          tags=["atividade3", f"versao-{versao}", caso["id"]], **FLUXO)
            saida = {**base, "erro": None, **r}
            status = "ok" if r["validacao"]["schema_valido"] else "schema_invalido"
        except Exception as e:  # registrado, não descartado
            saida = {**base, "erro": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc(),
                     "saida_bruta": "", "saida_final": None}
            status = "erro"
        destino.write_text(json.dumps(saida, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        registro["saidas"].append({"caso_id": caso["id"], "status": status, "arquivo": destino.name,
                                   "model_version": saida.get("model_version"),
                                   "trace_url": saida.get("trace_url")})
        print(f"[{versao}] {caso['id']}: {status}")
    registro["fim_utc"] = datetime.now(timezone.utc).isoformat()
    (VERSOES_DIR / versao / "execucao.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2),
                                                         encoding="utf-8")
    return registro


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--versao", nargs="+", choices=list(VERSOES), default=list(VERSOES))
    args = ap.parse_args()
    if config.PROVIDER == "groq" and not config.GROQ_API_KEY:
        raise SystemExit("GROQ_API_KEY ausente no .env (copie .env.example para .env).")
    if config.PROVIDER == "gemini" and not config.GEMINI_API_KEY:
        raise SystemExit("GEMINI_API_KEY ausente no .env.")
    registrar_prompts()
    sessao = "av3-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    for v in args.versao:
        executar_versao(v, sessao)
    try:
        from langfuse import get_client
        get_client().flush()
    except Exception:
        pass
    print("Próximo passo: python -m atividade3.scripts.preparar_avaliacao")


if __name__ == "__main__":
    main()
