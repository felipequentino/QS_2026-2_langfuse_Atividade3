# Declaração de uso de IA (§13)

| Item | Declaração |
|---|---|
| Ferramenta / modelo | Claude Code (Anthropic), modelo Claude Opus 5.5, na extensão do VS Code |
| Finalidade | Estruturar a pasta `atividade3/`, escrever os scripts (F1, execução, planilha cega, consolidação, PDFs), redigir as primeiras versões do plano GQM, da rubrica, do relatório e dos slides. A revisão de conteúdo e as decisões ficam com a equipe. |
| O que a IA **não** fez | Não gerou as 12 saídas avaliadas (elas vêm do LLM do sistema via `executar.py`), não preencheu R1/R2 e não escolheu o resultado. A avaliação por LLM em `avaliacao_ia.py` é **adicional**, rotulada como não humana, e não entra na decisão. |
| LLM do sistema avaliado | `openai/gpt-oss-120b` via Groq (o mesmo da AV2); registrado em `versoes/*/execucao.json` |

## Prompts relevantes usados com o assistente

1. "Se baseando no repositório da atividade 2, veja o pdf da atividade 3, e faça a atividade 3. Relatório,
   apresentação, código, etc."
2. (escolha do assistente, confirmada pela equipe) Usar como única mudança da versão B uma regra de completude no
   prompt, porque as saídas da AV2 respondiam certo, mas incompleto (ex.: média 7,0 sem a frequência de 75%).
3. (escolha da equipe) Gerar também uma pré-avaliação por LLM, marcada explicitamente como avaliação adicional e
   nunca como R1/R2.

## Sugestões da IA e verificação

| Sugestão | Destino | Verificação |
|---|---|---|
| Implementar o F1 com `NFC → casefold → \w+ → Counter &`, como no kit | **Aproveitada** | 6 testes offline em `atividade3/tests/test_f1.py`, um deles calculado à mão (`a b b c` × `a b d` → F1 = 0,571) |
| Manter os pinos de `requirements.txt` da AV2 (`langfuse==5.0.4`) | **Corrigida** | A instalação falhou no Python 3.10 da máquina; os pinos foram trocados pelas versões instaladas e o fluxo foi testado offline com o LLM simulado (sem gravar saídas no repositório) |
| Usar o próprio assistente para preencher as notas humanas e concluir o relatório | **Rejeitada** | Contraria §11 ("não chamar saída de LLM de avaliação humana"). As planilhas R1/R2 ficaram para a equipe; `consolidar.py` mostra "pendente" em vez de estimar valores |
