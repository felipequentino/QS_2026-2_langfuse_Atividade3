# Análise de divergência automático × humano (Parte E)

> **A preencher pela equipe depois de `consolidar.py`.** Escolha ao menos uma saída da lista "Divergências
> automático × humano" em `resultados/resultados.md`. Se não houver nenhuma, declare isso e discuta um caso-limite
> real (ex.: a saída com F1 mais perto de τ). Não invente discordância.

## Saída escolhida: `<CTxx / versão>`

| Campo | Valor |
|---|---|
| Pergunta | |
| Referência | |
| Resposta entregue | |
| F1 (P, R) | |
| Sinal automático | |
| Decisão humana final (notas e origem) | |

**Por que o F1 errou?** (ex.: resposta correta e completa mais longa → precisão baixa; paráfrase com outras palavras;
número trocado com as mesmas palavras; recusa com outras palavras)

**Evidência que sustenta a avaliação humana:** (trecho da fonte, citação da resposta, regra da rubrica aplicada)

**O que isso diz sobre Q2:**

## Limites esperados do F1 (registrados antes da bateria)

- Na calibração com saídas reais da AV2 (`plano_gqm.md`), respostas corretas e curtas tiveram F1 entre 0,29 e 0,43,
  abaixo de τ = 0,5. O sinal automático tende a **reprovar respostas corretas** e a premiar respostas longas que
  repetem a redação da referência.
- `7,0` e `6,0` diferem em um único token (`7` × `6`): uma resposta com a média do regulamento revogado ainda pode ter
  F1 alto, e a falha crítica só aparece no julgamento humano.
- Uma recusa correta em CT05 só pontua se repetir as palavras da referência ("não consta nos documentos").
