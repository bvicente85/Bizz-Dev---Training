---
Tags: 
  - Área: TI
  - Sub-área: Big Data
  - Tipo: Curso de Programação Científica / Engenharia de Dados
---

# PySpark - Processamento de Dados

## Visão Geral
A formação PySpark – Processamento de Dados é dirigida a Data Engineers, Analistas de Dados e Programadores Python que procurem escalar o processamento analítico para cenários de Big Data, lidando com volumes imensos de dados. O Apache Spark na sua interface PySpark tem a vertente robusta na otimização da escalabilidade do processamento nos clusters com eficiência ímpar. Com 3 dias focados em hands-on e programação prática, esta formação mergulha profundamente no ecossistema e abstrações core num ambiente Python nativo—desde manipulação de RDDs na teoria fundamental às SQL DataFrames, optimizações e processamentos interativos, Machine Learning e otimização por persistência nos Worker Nodes de Clusters em paralelo.

## Detalhes
- **Duração:** 3 dias
- **Link URL:** https://www.skolae-formacao.pt/formacao/pyspark-processamento-de-dados

## Objetivos e Ganhos
O que as equipas alcançam com a formação:
- Compreender a arquitetura de execução do Apache Spark em modelos clusterizados virtuais e locais.
- Executar abstrações distribuídas como RDD, Spark SQL e optimizações do Catalyst.
- Manipulação analítica de Dataframes Python paralelizadas utilizando SparkDataFrames.
- Manipular formatos como Parquet, Orc ou JSON de forma centralizada.
- Executar scripts na Spark Streaming usando streaming data de clusters analíticos.

## Estrutura do Programa
Os passos da jornada de aprendizagem:

1. **INTRODUÇÃO AO APACHE SPARK E ECOSSISTEMA**
   Conceitos de High-Performance Computing para Big Data e limitações do paradigma Hadoop MapReduce perante a in-memory architecture (Spark). Anatomia da plataforma com os workers e master executers, o driver program, gestão do ciclo DAGs, UI Spark para debbuging de processos.
2. **PROGRAMAÇÃO EM PYTHON**
   Noção essencial: Coleções Python standard vs arquitetura do RDD nativo distribuído na Worker Pool. Funções anónimas essenciais e lambda expressions perante RDD Maps, Filtros, Joins base e Reduces vs a paralelização de iterables globais por MapPartitions. Padrão básico do driver app e workers e limitações práticas.
3. **SPARK SQL E DATAFRAMES API (O ECOSSISTEMA MODERNIZADO)**
   A transição e razões do DataFrame API contra os antigos RDDs raw. Compreensão das conversões de Python nativo a Spark Catalyst. Definição do SparkSession, SparkContext legacy contra SparkSession Builder model, e leitura complexa num data flow Parquet com Schemas explicitos e Type Inferrings de JSON Arrays/CSV.
4. **OTIMIZAÇÃO DO PIPELINE DE BIG DATA**
   Partições explícitas: técnicas para controlo de OOM errors nos pipelines. Utilização das opções explicitas e otimizações automáticas. Tratamento das joins perigosas e broadcast de Lookup Tables a Nodes estáticos, além do Shuffle Read e Write Optimization nas UDFs em Python Nativo. Cache e armazenamento interativo, técnicas avançadas persist e unpersist.
5. **CASOS DE ESTUDO (A OTIMIZAÇÃO HANDS ON)**
   Reconhecimento das Skewed Partitions da UI Web da plataforma. Gestão e interpretação das métricas. Processamento interativo com Streaming DStream ou Structure Streaming API nativa do Pyspark, leitura interativa aos sockets nas streams base, ou Kafkas na entrada stream.

## Perfil do Formador (Requisitos)
Senior Data Engineer ou Big Data Architect atuante em pipeline PySpark nativo corporativo orientado para as otimizações, modelações avançadas clusterizadas em AWS EMR ou Databricks com experiência técnica robusta na pedagogia do processo analítico do Pyspark e da otimização do worker node de uma infraestrutura interligada.
