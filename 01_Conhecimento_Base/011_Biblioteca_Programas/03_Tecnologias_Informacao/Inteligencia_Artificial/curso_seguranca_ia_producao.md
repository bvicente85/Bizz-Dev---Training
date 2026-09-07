# Curso: Segurança da IA em Produção
**Área:** Inteligência Artificial / Cibersegurança | **Duração:** 21h (3 dias) | **Metodologia:** Técnica / Blue Team IA

## Descrição e Objetivos
Esta formação técnica foca-se na proteção de sistemas de Inteligência Artificial ao longo de todo o seu ciclo de vida. Utilizando o framework **MITRE ATLAS**, os participantes aprenderão a identificar vulnerabilidades em pipelines de dados, a detetar ataques adversariais em tempo real e a estruturar operações de segurança (SOC) específicas para modelos de IA em produção.

* Cartografar o ciclo de vida de modelos de IA e identificar zonas de risco segundo o **MITRE ATLAS**;
* Implementar controlos de acesso e rastreabilidade (IAM) em pipelines de treino e inferência;
* Detetar e mitigar ataques adversariais: **Envenenamento (Poisoning)**, **Evasão**, **Extração** e **Inversão de Modelo**;
* Integrar monitorização contínua de segurança baseada em **IoCs-IA** (Indicadores de Comprometimento);
* Elaborar e executar planos de resposta a incidentes de IA (Rollback, Re-treino seguro).

## Programa Detalhado

### 1. Cartografia de Riscos e Framework MITRE ATLAS
* Táticas e fases do ataque à IA: Reconhecimento, acesso ao pipeline e exploração do modelo;
* Mapeamento de fluxos de dados, artefactos e pontos de inferência;
* Segurança de infraestrutura: Separação de ambientes (DEV/TRAIN/PROD) e cifragem em repouso e trânsito.
* **Laboratório:** Modelização de um pipeline de IA e inventariação de ativos críticos.

### 2. Ataques Adversariais e Mitigação Técnica
* **Ataques à Integridade:** Data Poisoning (Envenenamento) e Data Falsification;
* **Ataques à Confidencialidade:** Model Extraction (Extração) e Model Inversion (Inversão);
* **Ataques de Evasão:** Manipulação de inputs na inferência;
* Defesas avançadas: Distilação, randomização e avaliação de robustez (**FGSM**, **PGD**).
* **Laboratório:** Geração de exemplos adversariais e testes de robustez do modelo.

### 3. Monitorização Contínua e SOC para IA
* Monitorização de desempenho vs. Monitorização de segurança;
* Deteção de anomalias estatísticas e padrões de pedidos anormais em APIs;
* Implementação de Dashboards de segurança com **Grafana** e **Prometheus**;
* **Laboratório:** Configuração de alertas para indicadores de comprometimento (IoCs-IA).

### 4. Resposta a Incidentes e Governação Sustentável
* Playbooks de resposta: Isolamento de modelos comprometidos e Rollback;
* Re-treino seguro: Purificação de datasets e validação de sanidade;
* Comunicação de incidentes e conformidade regulatória (AI Act);
* **Laboratório Final:** Simulação real de um incidente de comprometimento e execução do plano de resposta.

## Perfil do Formador / Notas de Venda
**Argumentos de Venda:** Este curso é essencial para empresas em setores críticos (Banca, Seguros, Saúde, Indústria 4.0) que já têm modelos de IA a servir clientes reais. O foco no **MITRE ATLAS** dá uma linguagem comum entre as equipas de Data Science e Cibersegurança, garantindo que a IA não se torna a "porta de entrada" para ataques à infraestrutura corporativa.
