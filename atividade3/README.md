# Atividade 3 — pasta de entrega

Pergunta norteadora: **uma mudança simples melhora a qualidade das respostas, e até que ponto a métrica automática
concorda com a avaliação humana?**

- **Fluxo:** assistente RAG da AV2 na configuração `hardened_v2` (Groq `openai/gpt-oss-120b`, T=0).
- **A:** prompt P2 1.0.0 da AV2 · **B:** A + restrição 8 (completude das condições e recusa com orientação). Única mudança.
- **Métrica:** F1 lexical por tokens, τ = 0,5 · **Humano:** rubrica 0–2 × 3 dimensões + falha crítica; R1 = 12, R2 = 4.
- **Decisão:** critério pré-registrado em [plano_gqm.md](plano_gqm.md); resultado em [resultados/resultados.md](resultados/resultados.md).

| Entregável (§12) | Onde |
|---|---|
| Plano GQM, τ e critério de decisão (pré-registro) | [plano_gqm.md](plano_gqm.md) |
| 6 perguntas, referências e fonte/trecho | [casos/casos.yaml](casos/casos.yaml) |
| Versões A/B + manifesto por versão | [versoes/A/](versoes/A/) · [versoes/B/](versoes/B/) (`prompt.txt`, `manifesto.yaml`, `execucao.json`) |
| 12 saídas brutas | [saidas/A/](saidas/A/) · [saidas/B/](saidas/B/) |
| Tabela automática + consolidada | [resultados/tabela_12.csv](resultados/tabela_12.csv) · [resultados/resultados.md](resultados/resultados.md) · [resultados/grafico.png](resultados/grafico.png) |
| Rubrica e 16 anotações humanas (12 R1 + 4 R2) + consenso | [rubrica.md](rubrica.md) · [anotacoes/](anotacoes/) |
| Avaliação adicional por LLM (não humana) | `anotacoes/IA_adicional.csv` (opcional) |
| Divergência / caso-limite | [docs/analise_divergencia.md](docs/analise_divergencia.md) |
| Ciclo de vida, diagrama e reconstrução | [docs/ciclo_vida.md](docs/ciclo_vida.md) |
| Contribuição e uso de IA | [docs/contribuicao.md](docs/contribuicao.md) · [docs/uso_ia.md](docs/uso_ia.md) |
| Relatório e slides | [relatorio/relatorio.pdf](relatorio/relatorio.pdf) · [apresentacao/slides.pdf](apresentacao/slides.pdf) |
| Vídeo | [../VIDEO.md](../VIDEO.md) |

## Código

| Script | Parte |
|---|---|
| `scripts/f1.py` | C: F1 lexical (NFC, casefold, `\w+`, multiconjunto) · testes em `tests/test_f1.py` |
| `scripts/calibracao_tau.py` | C: apoio à escolha de τ com saídas reais da AV2 |
| `scripts/executar.py` | B: 12 execuções, saídas brutas, `execucao.json` |
| `scripts/preparar_avaliacao.py` | D: planilhas cegas, chave e modelos R1/R2/consenso |
| `scripts/avaliacao_ia.py` | D: avaliação adicional por LLM (opcional, separada) |
| `scripts/consolidar.py` | E: tabela, denominadores, concordâncias, gráfico, decisão |
| `scripts/build_pdfs.py` | relatório e slides em PDF |

## Referências recuperáveis das versões
- A: `versoes/A/prompt.txt` (id `P2A`, igual ao `prompts/P2_estruturado.txt` da AV2) · B: `versoes/B/prompt.txt` (id `P2B`).
- `diff atividade3/versoes/A/prompt.txt atividade3/versoes/B/prompt.txt` mostra a única mudança.
- `versoes/<v>/execucao.json` registra commit, sha256 do prompt, provedor, modelo, `model_version` e datas da execução.
