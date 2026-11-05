# Procedimento do Resumo Diário de Clientes (17:00)

## Resumo Diário de Clientes (Daily Client Summary)
Sempre que receberes uma notificação do cron/timer com o prompt contendo "Resumo Diário de Clientes" (geralmente às 17:00), ou sempre que o utilizador pedir explicitamente o resumo diário, deves executar as seguintes ações:
1. Executa o script de recolha: Corre o comando `python "C:\Users\brunn\.gemini\antigravity\scratch\collect_today_conversations.py"` no terminal para extrair todas as conversas mantidas com o utilizador durante o próprio dia.
2. Lê os dados recolhidos: Lê o ficheiro JSON resultante em `C:\Users\brunn\.gemini\antigravity\scratch\today_conversations.json`.
3. Processa e resume em Português Europeu: Analisa os diálogos e cria um resumo estruturado de alto nível com:
   - **Clientes / Assuntos**: Identificação clara de cada cliente ou tema de conversa (ex: ALDI, Visualforma, etc.).
   - **Key Highlights**: Pontos principais e decisões tomadas.
   - **Pontos Importantes & Próximos Passos**: Ações a realizar, compromissos ou tarefas pendentes.
4. Grava no Obsidian: Cria um ficheiro Markdown em `c:\Users\brunn\OneDrive - GIE IFE\Desktop\Bruno\PESSOAL\Business Development Formação\03_Carteira_Clientes\Daily_Summaries\YYYY-MM-DD_Resumo_Diario.md` (substituindo YYYY-MM-DD pela data do dia atual) contendo o resumo gerado. Cria a diretoria `Daily_Summaries` se esta ainda não existir.
5. Apresenta o resumo no chat: Responde ao utilizador com o resumo completo formatado com um design premium e fornece um link local clicável para o ficheiro criado (ex: `[Abrir no Obsidian](file:///c:/Users/brunn/OneDrive%20-%20GIE%20IFE/Desktop/Bruno/PESSOAL/Business%20Development%20Formação/03_Carteira_Clientes/Daily_Summaries/YYYY-MM-DD_Resumo_Diario.md)`).
