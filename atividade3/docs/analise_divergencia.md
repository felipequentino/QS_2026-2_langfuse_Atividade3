# Análise de divergência automático × humano (Parte E)

Divergências automático × humano nas 12 decisões (concordância 9/12): **CT04/A, CT04/B e CT05/A**. Nas três o
F1 aprova (≥ 0,5) e a decisão humana (R1) reprova. Não houve o caso inverso (F1 reprova e o humano aprova): CT01/B e
CT06/A ficaram abaixo de τ e também foram reprovados por R1.

## Saída escolhida: CT04 / versão B

| Campo | Valor |
|---|---|
| Pergunta | Até quando posso solicitar o trancamento total da matrícula? |
| Referência | O trancamento total deve ser solicitado pelo portal acadêmico até o fim da 8ª semana do semestre letivo; depois disso, só por motivo de saúde comprovado por laudo. |
| Resposta entregue | O trancamento total deve ser solicitado pelo portal acadêmico até o fim da 8ª semana do semestre letivo. |
| F1 (P, R) | **0,783** (P = 1,000; R = 0,643) |
| Sinal automático | aprova (0,783 ≥ 0,5): o maior F1 entre as respostas que o humano reprovou |
| Decisão humana final (notas e origem) | **reprova**: C1 R2 S2, FC0 (R1). Justificativa de R1: "Informa o prazo da 8ª semana pelo portal mas omite a exceção por laudo de saúde" |

**Por que o F1 errou?** A resposta é um **prefixo literal** da referência: todos os tokens dela estão na referência
(P = 1,0), e falta só a segunda oração ("depois disso, só por motivo de saúde comprovado por laudo"), que custa recall
(0,643). O F1 média precisão e recall e não sabe que a parte que falta é uma **condição normativa**: um aluno que
leia essa resposta conclui que depois da 8ª semana não há saída, o que é falso. A resposta tem 18 tokens, todos na
referência, que tem 28; para o F1, os 10 tokens da exceção pesam o mesmo que quaisquer outros 10.

**Evidência que sustenta a avaliação humana:** o trecho recuperado e citado (DOC-TRANC#2) contém a exceção: "Após
esse prazo, o pedido só é aceito por motivo de saúde comprovado por laudo." A resposta não a menciona. Pela rubrica,
"parcial ou erro menor (falta uma condição da referência)" vale correção = 1, o que impede a aprovação. Não há falha
crítica: o que a resposta afirma está certo, só está incompleto.

**O mesmo padrão em CT04/A (F1 0,706) e CT05/A (F1 0,833).** Em CT05/A a abstenção está correta, mas a resposta não
orienta o discente a procurar a coordenação. R1 deu relevância 1 ("recusa sem orientar"), e o F1 continua alto porque
o resto da frase coincide com a referência.

**O que isso diz sobre Q2:** o F1 concordou com as pessoas em 9/12 decisões, mas **errou sempre para o mesmo lado**:
aprovou respostas incompletas cujas palavras coincidem com a referência. Ele separa bem "fala do assunto certo" de
"fala de outra coisa", e não separa "completa" de "incompleta" quando a parte omitida é curta. Por isso o F1 sozinho
não serve para decidir a troca de versão; no critério pré-registrado ele não entra na decisão.

## Caso-limite: o limiar τ decide CT01/B e CT06/A

CT01/B e CT06/A têm o **mesmo texto** ("A média mínima para aprovação por média é 7,0 (sete).") e F1 = 0,485, logo
abaixo de τ = 0,5. Aqui o automático e o humano concordam (os dois reprovam, R1 com C1: "omite os 75%"), mas por
pouco: com τ = 0,45 o sinal automático aprovaria essas respostas e a concordância cairia para 7/12. Uma concordância
de 9/12 depende de onde τ foi fixado.

## Observações factuais da execução (registradas antes das notas humanas)

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
