# Qualidade de Software — Atividade 3 · Métrica automática × avaliação humana (GQM)

**Equipe 01:** Bruno Saint Clair Silva Oliveira · Gabriel Bastos Pimentel · Gian Glauberty Santos Nascimento ·
João Felipe Quentino · João Victor Oliveira Moura · Leonardo de Souza Aragão · Renner do Nascimento Brito
**Vídeo:** ver [VIDEO.md](VIDEO.md) · **Relatório:** [atividade3/relatorio/relatorio.pdf](atividade3/relatorio/relatorio.pdf) ·
**Slides:** [atividade3/apresentacao/slides.pdf](atividade3/apresentacao/slides.pdf)

Tudo da AV3 está em [`atividade3/`](atividade3/README.md). As pastas `app/`, `data/` e `prompts/` são o fluxo da
AV2 reutilizado **sem alteração**, copiado de
[QS_2026-2_langfuse_Atividade2 @ 66dadb5](https://github.com/felipequentino/QS_2026-2_langfuse_Atividade2/tree/66dadb552638005f3013521458c4564af8e3a596).

## Como executar

```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                     # GROQ_API_KEY (obrigatória) e chaves do Langfuse (opcionais)

python -m pytest -q                                      # testes offline (F1 + validador da AV2), sem chave
python -m atividade3.scripts.executar                    # 6 casos × A/B = 12 saídas brutas (não sobrescreve)
python -m atividade3.scripts.preparar_avaliacao          # planilhas cegas + modelos R1.csv / R2.csv
#   >>> R1 preenche anotacoes/R1.csv (12) e R2 preenche anotacoes/R2.csv (4), sem abrir a chave nem resultados/
#   >>> se divergirem, registrar anotacoes/consenso.csv
python -m atividade3.scripts.avaliacao_ia                # OPCIONAL: avaliação adicional por LLM (não humana)
python -m atividade3.scripts.consolidar                  # tabela das 12, resumo, gráfico, decisão
python -m atividade3.scripts.build_pdfs                  # relatório e slides em PDF (Chrome headless)
```

## Segurança
`.env` está no `.gitignore`; nenhuma chave é versionada. Corpus 100% sintético (universidade fictícia "USN").
