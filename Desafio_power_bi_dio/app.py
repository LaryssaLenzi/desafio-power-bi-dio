import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro - DIO", layout="wide")

st.title("📊 Dashboard de Análise de Vendas (Power BI Challenge)")
st.markdown("Replicando o desafio da DIO usando Python e Streamlit")

# 1. Carregar os dados direto da biblioteca (Garante que não haverá erro de arquivo!)
@st.cache_data
def load_data():
    # Usamos o dataset 'stocks' ou criamos um mock rápido com os dados do desafio
    df = px.data.gapminder().query("year == 2007") # Dados mundiais reais do Plotly
    # Renomeando para bater com o seu desafio
    df = df.rename(columns={
        'country': 'Country',
        'gdpPercap': 'Sales',
        'pop': 'Units Sold',
        'continent': 'Segment'
    })
    # Criando uma coluna de lucro fictícia baseada em vendas
    df['Profit'] = df['Sales'] * 0.2
    return df

df = load_data()

# 2. Filtros na Barra Lateral
st.sidebar.header("Filtros")
segmento = st.sidebar.multiselect("Selecione o Segmento:", options=df["Segment"].unique(), default=df["Segment"].unique())
pais = st.sidebar.multiselect("Selecione o País:", options=df["Country"].unique(), default=df["Country"].unique())

df_selection = df.query("Segment == @segmento & Country == @pais")

# --- Layout das Linhas ---
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Vendas Totais", f"$ {df_selection['Sales'].sum():,.2f}")
with m2:
    st.metric("Lucro Total", f"$ {df_selection['Profit'].sum():,.2f}")
with m3:
    st.metric("Unidades Vendidas", f"{int(df_selection['Units Sold'].sum()):,}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Visual Mapa 1: Vendas por País")
    fig1 = px.scatter_geo(df_selection, locations="Country", locationmode='country names',
                         size="Sales", hover_name="Country", color="Sales",
                         projection="natural earth")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Visual Mapa 2: Soma de Lucro por País")
    fig2 = px.choropleth(df_selection, locations="Country", locationmode='country names',
                        color="Profit", hover_name="Country",
                        color_continuous_scale=px.colors.sequential.Greens)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Visual de Pizza: Lucro por Segmento")
fig3 = px.pie(df_selection, values='Profit', names='Segment', hole=0.4)
st.plotly_chart(fig3, use_container_width=True)
