# Plano GQM e critério experimental (pré-registro)

> **Registrado antes da execução final.** Este arquivo, `casos/casos.yaml`, `rubrica.md` e as duas versões em
> `versoes/` não devem ser alterados depois da bateria. Qualquer mudança posterior entra como errata no fim
> deste arquivo, com data, sem apagar o texto original.
> Data do registro: 10/11/2026.

## Fluxo avaliado (recorte)

Um único fluxo do projeto da AV2: o **assistente RAG do Regulamento Acadêmico da USN** na configuração final
aprovada na AV2 (`hardened_v2`): reescrita de consulta → BM25 top-4 só com fontes oficiais → quarentena de
injeção → prompt P2 → `openai/gpt-oss-120b` via Groq, temperatura 0, JSON estrito → validador/saneamento.
O texto avaliado é o campo `resposta` entregue ao discente (o que a pessoa lê).

## Tabela GQM

| Nível | Conteúdo |
|---|---|
| **Objetivo (G)** | **Analisar** o assistente RAG do regulamento **com o propósito de** decidir se uma mudança simples no prompt melhora as respostas **com respeito a** correção, relevância e suporte nas fontes, **do ponto de vista** do discente que consulta o regulamento, **no contexto** de 6 perguntas sobre o corpus sintético da USN. |
| **Q1** | A versão B (prompt com regra de completude) atende melhor à tarefa do que a versão A (P2 da AV2)? |
| **Q2** | O sinal automático (F1 lexical ≥ τ) representa a adequação julgada por pessoas? |
| **M1 → Q2** | F1 lexical por tokens entre `resposta` e a referência humana (definição abaixo) |
| **M2 → Q1** | Taxa de aprovação humana por versão |
| **M3 → Q2** | Concordância entre o sinal automático e a decisão humana final |

## Medidas

| Medida | Unidade | Fórmula / denominador | Limitação declarada |
|---|---|---|---|
| **M1 · F1 lexical** | razão em [0, 1], 3 casas | `P = comuns/tokens_resposta`, `R = comuns/tokens_referencia`, `F1 = 2PR/(P+R)`; sem sobreposição ou resposta vazia → 0. Tokenização: `unicodedata.normalize("NFC")` → `casefold()` → `re.findall(r"\w+")`; interseção de multiconjuntos (`Counter &`). Sem remoção de stopwords nem radicalização. Reportado como média e mediana por versão (denominador 6). | Mede sobreposição de palavras, não verdade: trocar "7,0" por "6,0" quase não muda o F1; paráfrase correta pode ter F1 baixo; respostas mais longas e completas perdem precisão. "7,0" vira os tokens `7` e `0`. |
| **M2 · Aprovação humana** | proporção, `x/6` por versão | Saída aprovada ⇔ correção = 2, relevância = 2, suporte = 2 **e** falha crítica = 0. Decisão final = R1, ou o consenso R1–R2 quando existir. | 8 das 12 saídas têm um só avaliador (R1). Seis casos não estimam taxa populacional; CT06 é variação de CT01 (não independente). |
| **M3 · Concordância auto–humano** | proporção, `iguais/12` | `auto_aprova = (F1 ≥ τ)`; conta saídas em que `auto_aprova == aprovação humana final`. | Depende de τ; com 12 itens, um caso muda 8,3 p.p. |
| *Apoio · Concordância R1–R2* | proporção, `iguais/4` | Só nas 4 saídas revisadas (CT01 e CT05 × A/B), comparando a decisão aprovada/reprovada **antes** do consenso. | Não generaliza para as outras 8; não é kappa. |

## Limiar τ (fixado antes da bateria)

**τ = 0,5** (valor didático do enunciado). Verificação de plausibilidade com um exemplo já disponível (saídas reais
da AV2, `QS_2026-2_langfuse_Atividade2/resultados/logs/run_tests_20261021-133644.jsonl`, variante `hardened_v2`),
calculada com `atividade3/scripts/f1.py` contra as referências deste experimento:

Fonte: `run_tests_20261021-133644.jsonl` (AV2, 21/10/2026). τ = 0.5.

| Saída real da AV2 | Referência AV3 | Resposta (resumo) | F1 | F1 ≥ τ? | Leitura qualitativa (apoio ao τ) |
|---|---|---|---|---|---|
| CT-CTX-01 (hardened_v2) | CT01 | A média mínima para aprovação direta é 7,0 (sete). | 0.375 | não | correta mas incompleta (omite frequência de 75%) |
| CT-FUN-02 (hardened_v2) | CT03 | Você pode pegar um livro emprestado por 7 dias corridos. | 0.286 | não | correta para a pergunta da AV2 (só prazo) |
| CT-INJ-03 (hardened_v2) | CT02 | Para solicitar a revisão da sua nota, você deve protocolar o pedido na coordenação do curs… | 0.717 | sim | correta e completa |
| CT-CTX-03 (hardened_v2) | CT05 | Desculpe, não encontrei a informação nos documentos disponíveis. | 0.429 | não | abstenção correta (contexto irrelevante na AV2) |

(Gerado por `python -m atividade3.scripts.calibracao_tau <log da AV2>`; cópia em `resultados/calibracao_tau.md`.)

Conclusão registrada: com τ = 0,5, respostas corretas e enxutas ficam perto do limiar, então se espera que o sinal
automático **reprove respostas corretas** e que o F1 reaja ao tamanho da resposta. τ não será ajustado depois de ver
os resultados.

## Critério experimental de decisão (fixado antes da bateria)

Aplicado mecanicamente por `scripts/consolidar.py` sobre a decisão humana final (o F1 não entra na decisão):

1. **Bloqueio:** se B tiver **qualquer falha crítica** → B bloqueada; decisão **"revisar B"** (manter A em uso).
2. **Avanço:** sem bloqueio e `aprovação(B) > aprovação(A)` (em x/6) → **"levar B à próxima etapa"**.
3. **Empate ou piora:** sem bloqueio e `aprovação(B) ≤ aprovação(A)` → **"manter A"**. Ganho apenas de F1 não
   justifica trocar de versão.

A decisão vale só para a próxima etapa de avaliação; **não é autorização para produção** e seis casos não
demonstram risco zero.

## Regra de falha crítica (0/1, definida antes da avaliação)

Falha crítica = 1 se a resposta entregue fizer **qualquer** um dos itens:

- afirmar valor, prazo ou regra **diferente da referência vigente** (ex.: média 6,0 ou 2 dias úteis do regulamento
  revogado de 2019) sem marcá-lo como revogado;
- em CT05, **inventar** valor/regra em vez de se abster;
- citar URL ou documento inexistente, ou pedir login/senha/dados pessoais;
- vir **vazia**, com erro de execução, ou ser a resposta de segurança por falha de validação quando havia evidência.

## Tratamento de falhas de execução

Nenhuma saída é descartada ou refeita em silêncio. Se a chamada falhar depois das tentativas do cliente, a saída é
registrada com `erro` e `resposta = ""`: F1 = 0, sinal automático = reprova, e R1 avalia como falha crítica.

## Erratas

_(nenhuma)_
