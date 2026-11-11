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

## Observações factuais da execução (antes das notas humanas)

Registradas a partir das saídas e do F1; **não são avaliação humana** e não antecipam as notas de R1/R2.

- **O efeito de B não foi uniforme.** CT01/A respondeu "7,0 (sete), com frequência mínima de 75 %"
  (F1 0,615), e CT01/B respondeu só "7,0 (sete)" (F1 0,485). Na variação CT06 ocorreu o inverso: A só "7,0" (0,485),
  B "7,0, exigindo frequência mínima de 75%" (0,667). A mesma regra produziu completude em um par e não no outro.
- **CT04 nas duas versões omite a exceção do laudo** que está na referência, e mesmo assim o F1 é alto
  (A 0,706; B 0,783 com P = 1,0): o F1 aprova uma resposta que pode ser parcial. É um candidato a divergência
  quando as notas humanas estiverem prontas.
- **CT05**: as duas versões se abstêm. B segue a regra 8 e orienta procurar a coordenação, o que leva o F1 a 0,950;
  A não orienta e tem F1 0,833.
- **Avaliação adicional por LLM (não humana)**: deu suporte 0 às duas abstenções de CT05, embora a rubrica atribua 2
  à "abstenção justificada". Também aprovou CT01/B e CT06/A, que omitem os 75%, e tratou CT04/A e CT04/B de forma
  diferente (reprovou A e aprovou B), quando as duas omitem o laudo. Exemplo concreto de por que o juiz LLM não
  substitui a avaliação humana [JUDGE].

## Limites esperados do F1 (registrados antes da bateria)

- Na calibração com saídas reais da AV2 (`plano_gqm.md`), respostas corretas e curtas tiveram F1 entre 0,29 e 0,43,
  abaixo de τ = 0,5. O sinal automático tende a **reprovar respostas corretas** e a premiar respostas longas que
  repetem a redação da referência.
- `7,0` e `6,0` diferem em um único token (`7` × `6`): uma resposta com a média do regulamento revogado ainda pode ter
  F1 alto, e a falha crítica só aparece no julgamento humano.
- Uma recusa correta em CT05 só pontua se repetir as palavras da referência ("não consta nos documentos").
