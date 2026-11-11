# Qualidade de Software — Atividade 3: métrica automática × avaliação humana (GQM) e versionamento

**Equipe 01:** Bruno Saint Clair Silva Oliveira · Gabriel Bastos Pimentel · Gian Glauberty Santos Nascimento ·
João Felipe Quentino · João Victor Oliveira Moura · Leonardo de Souza Aragão · Renner do Nascimento Brito<br>
**Entrega:** 11/11/2026 · **Apresentação:** 12/11/2026<br>
**Repositório:** {{repo_url}} (pasta `atividade3/`) · **Vídeo:** {{video_url}}<br>
**Base reutilizada:** assistente RAG da AV2 (`QS_2026-2_langfuse_Atividade2` @ `66dadb5`), sem reconstrução.

**Pergunta norteadora:** uma mudança simples melhora a qualidade das respostas, e até que ponto a métrica automática
concorda com a avaliação humana?

## 1. Contribuição dos integrantes

{{include ../docs/contribuicao.md}}

## 2. Recorte e plano GQM

{{include ../plano_gqm.md}}

## 3. Método

**Casos.** Seis casos finais em `casos/casos.yaml`: CT01–CT04 funcionais, CT05 sem evidência suficiente (a referência
é a abstenção) e CT06, variação de CT01 (sem acentos, "pra", "aprovdo"). Cada referência foi escrita a partir do
trecho da fonte e não de uma resposta do modelo. CT01, CT02 e CT06 recuperam também o regulamento revogado de 2019
(média 6,0; 2 dias úteis), o que testa correção factual com palavras quase iguais.

| Caso | Tipo | Pergunta | Fonte |
|---|---|---|---|
| CT01 | funcional | Qual a média mínima para ser aprovado por média? | DOC-AVA-2026#2 |
| CT02 | funcional | Qual o prazo para pedir revisão de nota? | DOC-AVA-2026#5 |
| CT03 | funcional | Quantos livros posso pegar emprestado na biblioteca e por quanto tempo? | DOC-BIBLIO#1 |
| CT04 | funcional | Até quando posso solicitar o trancamento total da matrícula? | DOC-TRANC#2 |
| CT05 | sem evidência | Qual o valor da bolsa de iniciação científica? | nenhuma |
| CT06 | variação de CT01 | qual a media minima pra ser aprovdo por media? | DOC-AVA-2026#2 |

**Versões.** A = prompt P2 1.0.0 da AV2, sem alteração de conteúdo. B = A + uma restrição (a única mudança):

> 8. Responda de forma completa e direta, em no máximo três frases: inclua todas as condições que o documento
> vigente associa à regra perguntada (valores, prazos, requisitos cumulativos, onde ou como solicitar e exceções).
> Ao recusar, diga que a informação não consta nos documentos disponíveis e oriente o discente a procurar a
> coordenação do curso.

Motivação: nas saídas reais da AV2 o P2 acertava, mas omitia condições (ex.: "A média mínima para aprovação direta
é 7,0 (sete)", sem a frequência de 75%) e recusava sem orientar. Modelo, parâmetros, recuperação, guardas, corpus e
casos são iguais nas duas versões (`scripts/comum.py: FLUXO`).

**Execução.** `scripts/executar.py` roda cada caso uma vez em A e uma vez em B (12 chamadas de geração e 12 de
reescrita de consulta), grava as 12 saídas brutas sem sobrescrever e registra falhas como saídas com erro.

**Métrica automática.** F1 lexical por tokens (`scripts/f1.py`), calculado sobre o campo `resposta` entregue ao
discente, com τ = 0,5 fixado antes da bateria. **Avaliação humana.** Rubrica de 3 dimensões (0–2) e falha crítica
(`rubrica.md`), planilhas cegas com ids embaralhados (`scripts/preparar_avaliacao.py`), R1 nas 12 saídas e R2,
independente, em CT01 e CT05 × A/B (16 anotações).

## 4. Resultados

{{include ../resultados/resultados.md}}

## 5. Divergência ou caso-limite

{{include ../docs/analise_divergencia.md}}

## 6. Ciclo de vida e versionamento

{{include ../docs/ciclo_vida.md}}

## 7. Decisão e questões de análise

**Decisão (critério pré-registrado):** {{decisao}}

- **B melhorou a qualidade humana ou só a métrica?** {{q_melhoria}}
- **Qual saída mostra melhor o limite do F1?** Ver a seção 5; a calibração com saídas da AV2 já mostrava respostas
  corretas abaixo de τ.
- **É possível reconstruir uma saída pelo manifesto?** Sim para código, prompt (sha256), corpus, casos, parâmetros e
  contexto usado; **não** para a revisão do modelo hospedado (`openai/gpt-oss-120b` no Groq), que a API não permite
  congelar. Ficam registrados `model_version` e a data.
- **Que sinal acompanhar e como voltar a A?** Falha crítica (alvo 0), taxa de recusa com evidência, tamanho da
  resposta e aprovação humana em amostras novas. O retorno a A é trocar `P2B` por `P2A`; o arquivo de A nunca é
  editado.

## 8. Limitações

- Seis casos e uma execução por caso/versão: os resultados mostram tendência, não taxa. CT06 depende de CT01.
- 8 das 12 decisões vêm de um único avaliador (R1); a concordância R1–R2 cobre só 4 saídas.
- Cegamento parcial: o estilo de B (mais longo, recusa com orientação) pode ser reconhecido; CT01 e CT06 têm a
  mesma referência.
- O modelo hospedado não é congelável e a temperatura 0 não garante determinismo; a reescrita de consulta também é
  gerada pelo LLM.
- Corpus sintético e pequeno; F1 sem stopwords nem radicalização favorece respostas que repetem a redação da
  referência.
- A decisão vale só para a próxima etapa de avaliação, não para produção.

## 9. Uso de IA

{{include ../docs/uso_ia.md}}

## 10. Referências

- [GQM] van Solingen, R.; Basili, V.; Caldiera, G.; Rombach, H. D. *Goal Question Metric (GQM) Approach*.
  Encyclopedia of Software Engineering, 2002. https://onlinelibrary.wiley.com/doi/abs/10.1002/0471028959.sof142
- [NIST] NIST. *AI 600-1: Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence
  Profile*, 2024. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- [JUDGE] Zheng, L. et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, 2023.
  https://arxiv.org/abs/2306.05685
- Repositório da AV2 (fluxo reutilizado): https://github.com/felipequentino/QS_2026-2_langfuse_Atividade2
