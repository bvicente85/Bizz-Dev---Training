# Regras do Projeto (Business Development Formação)

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

## Regras de Qualificação e Escrita (SPIN & Contactos Telefónicos)
Sempre que redigires e-mails de qualificação de oportunidades (inbound ou seguimento) ou fizeres referências a tentativas de contacto telefónico:
1. **Adaptabilidade da Saudação:** A saudação inicial deve adequar-se ao perfil do cliente e ao tom do contacto. Usa *"Estimado [Nome]"* para entidades formais/públicas (ex: SIRP, Ministérios) ou quando o pedido inicial for muito formal. Usa *"Olá [Nome]"* ou *"Caro [Nome]"* em circunstâncias normais, para clientes recorrentes ou quando o pedido inicial tiver um tom mais leve e informal.
2. **Omitir Ausência de Retorno:** Nunca menciones que o cliente não atendeu ou que não retornou uma chamada que tinha ficado prometida. Escreve apenas de forma limpa e sem cobrança: *"No seguimento da minha tentativa de contacto de ontem/hoje,..."*
3. **Qualificação Simplificada:** Formula as perguntas em parágrafos separados ou bullets limpos, sem numeração rígida ou negritos pesados.
   - A primeira pergunta deve sempre enquadrar quem são os destinatários e o número de formandos.
   - **Adaptação Contextual:** Se a lead for claramente escrita no singular/individual, adapta a pergunta para clarificar o âmbito (ex: *"Esta formação é só para si ou pretende incluir também outros colegas do [Nome da Empresa]?"*). Caso contrário, usa a fórmula genérica (ex: *"Qual é o perfil dos destinatários desta ação (equipa de comunicação, assessores, direção) e quantos formandos?"*).
4. **CTA Teams Direto:** Para propor a reunião de diagnóstico, sugere de forma simples e sem indicação de tempos ou links rígidos. Exemplos recomendados: *"Se for mais prático alinharmos isto numa conversa via Teams."* ou *"Se for mais prático podemos explorar este tema numa conversa via Teams em data e hora que lhe seja mais favorável."*
5. **Fecho Objetivo:** Termina sempre com: *"Fico a aguardar o seu feedback."*
6. **Aplicação Flexível das Regras:** O espírito das regras (ausência de cobrança, concisão, fluidez) deve prevalecer sobre a replicação literal de frases pré-definidas. O e-mail final deve soar natural e comercialmente polido.
7. **Follow-up a Clientes Sem Resposta (Soft Break-up):** Quando um cliente deixar de responder após envio de informação ou proposta (*ghosting*), o e-mail de follow-up deve adotar uma abordagem de "Limpeza de Arquivo", dando "permissão para fechar" o assunto e retirando a culpa ao cliente. Usa a estrutura: *"Estou a fechar os projetos em aberto deste trimestre. Como não voltei a ter feedback, vou assumir que o vosso foco interno está noutras áreas e vou encerrar este assunto do nosso lado. Se a situação mudar, sinta-se à vontade para reabrir o contacto."* Evita formalismos excessivos ("reiterar disponibilidade") e não faças cobrança da falta de resposta.

## Diretrizes Ambientais e de Infraestrutura (Windows & CLI)
Sempre que executares operações de ficheiro ou pesquisas no terminal:
1. **Caminhos Longos (Path Length Limit):** No Windows, caminhos de pastas com mais de 260 caracteres falham na leitura padrão do sistema operativo. Deves preferir correr scripts Python para ler/escrever ficheiros e usar o prefixo UNC `\\\\?\\` antes dos caminhos absolutos (ex: `\\\\?\\C:\\Users\\...`) para ignorar este limite.
2. **Ausência de Ferramentas de Consola:** Não assumas que comandos de terceiros (como `grep`, `git`, etc.) estão instalados ou no `%PATH%` do Windows. Se um comando falhar ou precisares de fazer pesquisas de texto, escreve scripts simples em Python que utilizem apenas bibliotecas nativas para garantir o sucesso da execução.
3. **Pesquisas de Texto Precisas:** Ao pesquisares siglas, acrónimos ou palavras-chave específicas em ficheiros (seja através de ferramentas integradas ou scripts Python), deves usar sempre correspondência exata de palavras inteiras (*word boundaries*, ex: `\bPALAVRA\b` em RegEx) ou ter em conta *case-sensitivity* para evitar falsos positivos (por exemplo, confundir a sigla 'DISC' com palavras comuns como 'discuss' ou 'discover'). Nunca utilizes verificações simples de substring (ex: `'DISC' in texto`) sem garantir os limites da palavra.



## Marca Oficial e Identidade
A empresa parceira representa-se exclusivamente como **Skolae** ou **SKOLAE Formação**. Nunca deves utilizar grafias erradas foneticamente (como "Scollai" ou "Scolae") na redação, revisão de propostas, e-mails, atas ou relatórios.

## Rigor na Escrita em Inglês B2B
Sempre que redigires comunicações em inglês (e-mails, propostas ou abordagens), deves aplicar estritamente e por defeito as regras do guia `bd_estilo_escrita.md`:
* **Contrações Obrigatórias:** Usa sempre contrações (*we've, you'll, it's, don't*) para soar autêntico e humano. A ausência de contrações é considerada falha crítica.
* **Aberturas Naturais:** Iniciar e-mails com *"Hi [Nome]"*, rejeitando fórmulas excessivamente formais como *"Dear"*.
* **Proibição de Conectores IA:** Banir conectores académicos ou de inteligência artificial (*Furthermore, Moreover, Indeed, Therefore*).
* **Tom:** Adotar um estilo coloquial-profissional, direto e empático, utilizando *phrasal verbs* comuns em ambiente de negócios internacional.

## Abordagem a Novos Contactos (Cold Emails / Prospeção)
Sempre que o utilizador pedir para redigir um "primeiro e-mail", uma "abordagem" a um novo contacto ou um "cold email":
1. **Uso Obrigatório de Templates:** Deves seguir rigorosamente a estrutura definida no `bd_estilo_escrita.md` (Template A - Contactos Frios, ou Template H - Sequência de Prospeção). Não inventes templates novos.
2. **Estrutura Base:** O e-mail deve conter uma apresentação direta ("O meu nome é Bruno Vicente..."), a validação do interlocutor ("Tenho a indicação de que lidera... / Gostaria de confirmar se este tema deve ser tratado consigo..."), o foco nas prioridades para os próximos meses (sem vender soluções logo de imediato) e um Call to Action leve ("breve conversa via Teams de 15 minutos" condicionado por um "Caso seja a pessoa indicada...").
3. **Omissão de Contexto Colateral:** Nunca menciones pedidos de empresas subsidiárias, colegas de outras delegações ou eventos passados como "gancho" inicial, a menos que o utilizador peça explicitamente para usar essa alavanca. Por defeito, a abordagem deve ser tratada como um contacto 100% "frio" e focado apenas no interlocutor atual.

## Alertas Financeiros e Logísticos (Propostas & Custos Diretos)
1. **Localização e Deslocações (Sede em Lisboa):** A sede da SKOLAE situa-se em Lisboa. Sempre que uma formação presencial decorrer fora da Grande Lisboa (ex: Torres Vedras, Porto, Évora, etc.), deves **emitir obrigatoriamente um alerta** para verificar se os custos de deslocação, portagens, alimentação e estadia do formador foram devidamente considerados na proposta financeira ou ressalvados como encargo do cliente.
2. **Materiais Didáticos Especiais (Tabuleiros / Jogos Pedagógicos):** Em formações que utilizem dinâmicas físicas específicas (como o tabuleiro do *Jogo dos Exploradores* no programa de Liderança Situacional), deves **alertar expressamente para o custo do tabuleiro/kit pedagógico**, garantindo que este custo direto não é omitido no cálculo da margem e na proposta financeira.

## Retificação de Propostas e Ajustes de Preço (Transparência sem "Cozinha Interna")
Sempre que for necessário comunicar a um cliente uma retificação de valor ou subida de preço decorrente de um erro, lapso ou incorreção de cálculo prévio (mesmo que a ação já esteja validada ou adjudicada):
1. **Proibição de "Cozinha Interna":** Nunca detalhar custos horários de formadores, margens comerciais, despesas internas ou imputar culpas a colegas anteriores.
2. **Transparência e Objetividade Direta:** Assumir de forma limpa que foi identificada uma incorreção no cálculo inicialmente considerado e apresentar com clareza os dois valores (ex: *"passando de X € para Y €"*).
3. **Reconhecimento Empático:** Reconhecer com maturidade que a alteração surge após a intenção manifestada de avançar, justificando que a partilha direta dessa informação é feita previamente para validar se o cliente pode prosseguir nessas condições.
4. **Tom e Concisão:** O e-mail deve ser curto, sóbrio e empático, terminando sempre com a disponibilidade para esclarecer dúvidas e o fecho objetivo: *"Fico a aguardar o seu feedback."*

## Gestão de Memória Comercial (Phase 3.5 - Client Intelligence)
Sempre que criares ou atualizares a ficha de inteligência de um cliente (ex: `[Cliente]_Intelligence.md`), deves garantir que o ficheiro começa obrigatoriamente com um bloco YAML Frontmatter. Este bloco serve para estruturar os dados para futura exportação e integração com CRMs (ex: Odoo).
O bloco deve ter a seguinte estrutura mínima:
```yaml
---
status: [Ativo / Frio / Fechado / Adormecido]
core_business: [Breve descrição da área de negócio]
decisores: [Lista de nomes e cargos]
data_ultima_interacao: [YYYY-MM-DD]
areas_interesse: [Lista de tags de competências, ex: Liderança, Vendas, Excel]
---
```
Isto garante que cada cliente funciona como um micro-banco de dados independente, exportável e imediatamente legível por máquinas.

