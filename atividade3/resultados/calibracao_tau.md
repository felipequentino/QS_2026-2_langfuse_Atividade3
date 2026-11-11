Fonte: `run_tests_20261021-133644.jsonl` (AV2, 21/10/2026). τ = 0.5.

| Saída real da AV2 | Referência AV3 | Resposta (resumo) | F1 | F1 ≥ τ? | Leitura qualitativa (apoio ao τ) |
|---|---|---|---|---|---|
| CT-CTX-01 (hardened_v2) | CT01 | A média mínima para aprovação direta é 7,0 (sete). | 0.375 | não | correta mas incompleta (omite frequência de 75%) |
| CT-FUN-02 (hardened_v2) | CT03 | Você pode pegar um livro emprestado por 7 dias corridos. | 0.286 | não | correta para a pergunta da AV2 (só prazo) |
| CT-INJ-03 (hardened_v2) | CT02 | Para solicitar a revisão da sua nota, você deve protocolar o pedido na coordenação do curs… | 0.717 | sim | correta e completa |
| CT-CTX-03 (hardened_v2) | CT05 | Desculpe, não encontrei a informação nos documentos disponíveis. | 0.429 | não | abstenção correta (contexto irrelevante na AV2) |
