# Diretrizes de Sistema, Ambiente e Repositório

## Diretrizes Ambientais e de Infraestrutura (Windows & CLI)
Sempre que executares operações de ficheiro ou pesquisas no terminal:
1. **Caminhos Longos (Path Length Limit):** No Windows, caminhos de pastas com mais de 260 caracteres falham na leitura padrão do sistema operativo. Deves preferir correr scripts Python para ler/escrever ficheiros e usar o prefixo UNC `\\\\?\\` antes dos caminhos absolutos (ex: `\\\\?\\C:\\Users\\...`) para ignorar este limite.
2. **Ausência de Ferramentas de Consola:** Não assumas que comandos de terceiros (como `grep`, `git`, etc.) estão instalados ou no `%PATH%` do Windows. Se um comando falhar ou precisares de fazer pesquisas de texto, escreve scripts simples em Python que utilizem apenas bibliotecas nativas para garantir o sucesso da execução.
3. **Pesquisas de Texto Precisas:** Ao pesquisares siglas, acrónimos ou palavras-chave específicas em ficheiros (seja através de ferramentas integradas ou scripts Python), deves usar sempre correspondência exata de palavras inteiras (*word boundaries*, ex: `\bPALAVRA\b` em RegEx) ou ter em conta *case-sensitivity* para evitar falsos positivos (por exemplo, confundir a sigla 'DISC' com palavras comuns como 'discuss' ou 'discover'). Nunca utilizes verificações simples de substring (ex: `'DISC' in texto`) sem garantir os limites da palavra.

---

## Protocolo de Integridade e Atualização do Repositório (Workflow de Manutenção)
Sempre que uma nova interação com cliente (notas de reunião, atas Granola, e-mails recebidos/enviados, decisões, próximos passos) for processada para atualização no GitHub:
1. **Exclusividade de Escrita:** O `Chief_of_Staff` é o único agente com capacidade de escrita. Todos os especialistas (`Knowledge_Specialist`, `Commercial_Specialist`, `Learning_Solution_Specialist`) são estritamente *read-only*.
2. **Auditoria Factual Prévia Obrigatória:** Antes de qualquer proposta de alteração, o `Knowledge_Specialist` deve obrigatoriamente auditar a informação contra os ficheiros existentes da conta para verificar se o cliente existe, identificar novidades reais, detetar duplicações e identificar conflitos.
3. **Proposta de Alteração Estruturada (Diff Proposal):** O sistema deve apresentar sempre uma proposta discriminada (`[NOVO]`, `[MODIFICAR]`, `[SEM ALTERAÇÕES]`) identificando os ficheiros e secções exatas afetadas.
4. **Portão de Confirmação Obrigatório (User Approval Gate):** É estritamente proibido escrever no repositório sem a confirmação e validação explícita do utilizador no chat.
5. **Edição Cirúrgica Obrigatória:** Usar sempre substituição cirúrgica de blocos de texto (`replace_file_content`). É proibido sobrescrever ficheiros completos quando uma alteração cirúrgica for viável.
6. **Criação de Ficheiros (`write_to_file`):** Permitida exclusivamente para novas atas/relatórios de reuniões (`034_Reunioes_Clientes/YYYY-MM/meeting-report-...md` ou na pasta do cliente) expressamente aprovadas. É expressamente **proibido criar automaticamente novas pastas de clientes ou novas estruturas de diretórios**; perante um cliente inexistente no repositório, o sistema deve alertar o utilizador e aguardar instruções prévias.
7. **`meeting_notes.md` é Estritamente Append-Only:** As notas de reuniões anteriores nunca são apagadas ou modificadas; novos resumos são sempre acrescentados cronologicamente no final.
8. **Preservação de Histórico:** O registo cronológico de interações (`_progress.md`) nunca pode ser truncado ou apagado.
9. **Visibilidade de Conflitos:** Qualquer contradição ou divergência de dados entre a nova interação e o histórico prévio deve ser explicitamente sinalizada para decisão do utilizador, nunca sendo resolvida de forma silenciosa ou automática.
10. **Zero Inferências em Ficheiros Factuais:** Hipóteses ou deduções do modelo nunca podem ser gravadas nos ficheiros de factos (`context.md`, `progress.md`, `meeting_notes.md`).
11. **Preservação Estrutural:** Manter a hierarquia de pastas (`031_Bases_Dados`, `032_Clientes`, `033_Pedidos_Informacao`, `034_Reunioes_Clientes`) e a segregação funcional dos ficheiros (`context.md`, `progress.md`, `meeting_notes.md`).
12. **Zero Git Ops & Preservação de Chats:** Não efetuar commits/pushes automáticos nem apagar ou alterar conversas antigas.
