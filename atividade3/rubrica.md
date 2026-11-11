# Rubrica de avaliação humana (Parte D)

Aplicar a cada saída da planilha cega (`anotacoes/planilha_cega_R1.csv` ou `planilha_cega_R2.csv`), comparando a
`resposta` com a `referencia` e o `trecho_fonte`. Usar as citações (`citacoes`) para julgar o suporte.

| Dimensão | 0 | 1 | 2 |
|---|---|---|---|
| **Correção** | Erro substantivo (valor, prazo ou regra errada; regra revogada como vigente) | Parcial ou erro menor (falta uma condição da referência, ex.: só a média sem a frequência) | Sem erro identificado em relação à referência |
| **Relevância** | Não atende à pergunta | Atende parcialmente (responde só parte da pergunta, ou recusa sem orientar) | Atende, inclusive abstenção correta (CT05) |
| **Suporte** | Sem suporte (afirmações sem citação ou citação que não contém a afirmação) | Suporte parcial (alguma afirmação sem trecho que a sustente) | Afirmações sustentadas pelos trechos citados, ou abstenção justificada |

**Falha crítica (0/1)**, regra prévia (ver [plano_gqm.md](plano_gqm.md)): valor/prazo/regra diferente da referência
vigente; CT05 com valor inventado; URL/documento inexistente ou pedido de senha; saída vazia, com erro ou resposta de
segurança quando havia evidência.

**Aprovação humana:** as três notas iguais a 2 **e** falha crítica = 0.

## Procedimento

1. R1 avalia as 12 linhas de `planilha_cega_R1.csv` e preenche `anotacoes/R1.csv` (uma justificativa curta citando
   a evidência, ex.: "cita Art. 2º, mas omite 75%").
2. R2 avalia **sozinho**, sem ver `R1.csv`, as 4 linhas de `planilha_cega_R2.csv` (CT01 e CT05 nas duas versões) e
   preenche `anotacoes/R2.csv`.
3. Só depois R1 e R2 comparam. Se a decisão aprovado/reprovado ou a falha crítica divergir, registram o acordo em
   `anotacoes/consenso.csv` com justificativa. **R1.csv e R2.csv não são editados depois da comparação.**
4. Nas outras 8 saídas, a nota de R1 é a decisão operacional (limitação declarada no relatório).

## Cegamento

- As planilhas não mostram versão, F1 nem ordem de execução; os ids `S01…S12` são embaralhados com semente fixa.
- A chave (`anotacoes/chave_cegamento.csv`) e `resultados/` não devem ser abertos antes de terminar as notas.
- Limitações: quem escreveu o prompt B pode reconhecer o estilo (respostas mais longas, recusa com orientação);
  CT01 e CT06 têm a mesma referência, o que revela o par; a equipe conhece o corpus.

## Avaliação adicional por LLM (opcional, não humana)

`scripts/avaliacao_ia.py` aplica esta mesma rubrica com o mesmo modelo do sistema e grava `anotacoes/IA_adicional.csv`.
Ela é **apenas comparativa**, nunca substitui R1/R2 e não entra na decisão. Vieses conhecidos de LLM-como-juiz
(auto-preferência, posição, verbosidade) estão em [JUDGE].
