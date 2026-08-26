# Arquivo de Contas (Clientes Inativos)

Esta pasta serve para armazenar todo o histórico de clientes que estão dados como "Perdidos", "Inativos" ou sem perspetivas a curto prazo (mais de X meses de inatividade).

**Objetivo:** Ao mover as contas inativas da pasta principal de Clientes para aqui, reduzimos o ruído nas pesquisas e poupamos os *tokens* de contexto do Agente Principal, garantindo que o seu foco de processamento e latência recai apenas sobre a carteira de vendas ativa.

O Agente Principal moverá as contas para esta diretoria sempre que for invocada a `Skill_Manutencao_Contas`.
