#!/usr/bin/env python
# coding: utf-8

# # Exercícios 
# 
# Utilize os arquivos do **RECLAME AQUI** e crie um dashboard com algumas caracteristicas. 
# 
# Empresas: 
# - Hapvida
# - Nagem
# - Ibyte
# 
# O painel deve conter tais informações: 
# 
# 1. Série temporal do número de reclamações. 
# 
# 2. Frequência de reclamações por estado. 
# 
# 3. Frequência de cada tipo de **STATUS**
# 
# 4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**) 
# 
# 
# Alguns botões devem ser implementados no painel para operar filtros dinâmicos. Alguns exemplos:: 
# 
# 1. Seletor da empresa para ser analisada. 
# 
# 2. Seletor do estado. 
# 
# 3. Seletor por **STATUS**
# 
# 4. Seletor de tamanho do texto 
# 
# Faça o deploy da aplicação. Dicas: 
# 
# https://www.youtube.com/watch?v=vw0I8i7QJRk&list=PLRFQn2r6xhgcDMhp9NCWMqDYGfeeYsn5m&index=16&t=252s
# 
# https://www.youtube.com/watch?v=HKoOBiAaHGg&t=515s
# 
# Exemplo do github
# https://github.com/jlb-gmail/streamlit_teste
# 
# 
# **OBSERVAÇÃO**
# 
# A resposta do exercicio é o link do github e o link da aplicação. Coloque-os abaixo.  
# 
# 

# Bibliotecas
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# Importando os dados
df_ibyte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_nagem = pd.read_csv('RECLAMEAQUI_NAGEM.csv')

df_ibyte["EMPRESA"] = "IBYTE"
df_hapvida["EMPRESA"] = "HAPVIDA"
df_nagem["EMPRESA"] = "NAGEM"

df_total = pd.concat([df_ibyte, df_hapvida, df_nagem], ignore_index=True)

# Criando o Dashboard
st.sidebar.title("DASHBOARDS BIBLIOTECAS PYTHON/R")
st.sidebar.subheader("MBA em Ciência de Dados - Unifor")
st.sidebar.subheader("Aluno: Paulo Victor Sales Araujo")

filtro_empresa = df_total['EMPRESA'].unique()

st.sidebar.title('Filtros')
painel = st.sidebar.radio('Filtre o Painel', [
    'Série temporal do número de Reclamações.',
    'Frequência de reclamações por Municipio.',
    'Frequência de cada tipo de Status',
    'Distribuição do tamanho do Texto'], key='painel')

botao_empresa = st.sidebar.radio("Filtre a Empresa", filtro_empresa, key='filtro_empresa')

estados = df_total['LOCAL'].unique()
botao_estado = st.sidebar.selectbox('Filtre por Estado', ['Todos'] + list(estados), key='filtro_estado')

df_filtrado_empresa = df_total[df_total['EMPRESA'] == botao_empresa]

# Aplicando o filtro de estado, exceto no painel de Frequência por Município
if botao_estado != 'Todos' and painel != 'Frequência de reclamações por Municipio.':
    df_filtrado_empresa = df_filtrado_empresa[df_filtrado_empresa['LOCAL'] == botao_estado]

cor_tema = {'NAGEM': 'blue', 'IBYTE': 'red', 'HAPVIDA': 'orange'}
cor_selecionada = cor_tema.get(botao_empresa, 'gray')
sns.set(style="whitegrid")

if painel == 'Série temporal do número de Reclamações.':
    st.title('Série temporal do número de reclamações')
    df_filtrado_empresa['DATA'] = pd.to_datetime(df_filtrado_empresa[['ANO', 'MES', 'DIA']].rename(columns={'ANO': 'year', 'MES': 'month', 'DIA': 'day'}))
    serie_temporal = df_filtrado_empresa.groupby('DATA').size().reset_index(name='Reclamações')
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='DATA', y='Reclamações', data=serie_temporal, color=cor_selecionada)
    plt.title(f'Série Temporal do Número de Reclamações - {botao_empresa}', fontsize=14)
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Número de Reclamações', fontsize=12)
    st.pyplot(plt)
    plt.clf()

elif painel == 'Frequência de reclamações por Municipio.':
    st.title('Frequência de reclamações por Municipio')
    frequencia_por_estado = df_filtrado_empresa['LOCAL'].value_counts().reset_index().head(20)
    frequencia_por_estado.columns = ['Estado', 'Reclamações']
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Reclamações', y='Estado', data=frequencia_por_estado, palette=[cor_selecionada])
    plt.title(f'Frequência de Reclamações por Municipio - {botao_empresa}', fontsize=14)
    plt.xlabel('Número de Reclamações', fontsize=12)
    plt.ylabel('Estado', fontsize=12)
    st.pyplot(plt)
    st.table(frequencia_por_estado)
    plt.clf()

elif painel == 'Frequência de cada tipo de Status':
    st.title('Frequência de cada tipo de Status')
    frequencia_por_status = df_filtrado_empresa['STATUS'].value_counts().reset_index()
    frequencia_por_status.columns = ['Status', 'Reclamações']
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Reclamações', y='Status', data=frequencia_por_status, palette=[cor_selecionada])
    plt.title(f'Frequência de Cada Tipo de Status - {botao_empresa}', fontsize=14)
    plt.xlabel('Número de Reclamações', fontsize=12)
    plt.ylabel('Status', fontsize=12)
    st.pyplot(plt)
    st.table(frequencia_por_status)
    plt.clf()

elif painel == 'Distribuição do tamanho do Texto':
    st.title('Distribuição do tamanho do Texto')
    df_filtrado_empresa['TAMANHO_DESCRICAO'] = df_filtrado_empresa['DESCRICAO'].apply(len)
    plt.figure(figsize=(12, 6))
    sns.histplot(df_filtrado_empresa['TAMANHO_DESCRICAO'], bins=30, color=cor_selecionada, kde=True)
    plt.title(f'Distribuição do Tamanho das Descrições para {botao_empresa}', fontsize=14)
    plt.xlabel('Tamanho do Texto', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    st.pyplot(plt)
    plt.clf()
