import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard Financeiro - DIO", layout="wide")

st.title("📊 Dashboard de Análise de Vendas (Power BI Challenge)")
st.markdown("Replicando o desafio da DIO usando Python e Streamlit")

# 1. Carregar os dados
@st.cache_data
def load_data():
    # Adicionamos o sep=';' para o padrão do Excel brasileiro
    df = pd.read_csv("dados.csv", sep=';') 
    return df


df = load_data()

# 2. Filtros na Barra Lateral
st.sidebar.header("Filtros")
segmento = st.sidebar.multiselect("Selecione o Segmento:", options=df["Segment"].unique(), default=df["Segment"].unique())
pais = st.sidebar.multiselect("Selecione o País:", options=df["Country"].unique(), default=df["Country"].unique())

df_selection = df.query("Segment == @segmento & Country == @pais")

# --- Layout das Linhas ---

# Linha 1: Métricas Principais
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Vendas Totais", f"$ {df_selection['Sales'].sum():,.2f}")
with m2:
    st.metric("Lucro Total", f"$ {df_selection['Profit'].sum():,.2f}")
with m3:
    st.metric("Unidades Vendidas", f"{int(df_selection['Units Sold'].sum()):,}")

st.divider()

# Linha 2: Os Visuais do Desafio
col1, col2 = st.columns(2)

with col1:
    st.subheader("Visual Mapa 1: Vendas e Unidades por País")
    # Agrupando por país para o mapa
    df_map1 = df_selection.groupby("Country").agg({"Sales": "sum", "Units Sold": "sum"}).reset_index()
    fig1 = px.scatter_geo(df_map1, locations="Country", locationmode='country names',
                         size="Sales", hover_name="Country", 
                         hover_data=["Units Sold"], color="Sales",
                         projection="natural earth", title="Soma de Vendas e Unidades")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Visual Mapa 2: Soma de Lucro por País")
    df_map2 = df_selection.groupby("Country")["Profit"].sum().reset_index()
    fig2 = px.choropleth(df_map2, locations="Country", locationmode='country names',
                        color="Profit", hover_name="Country",
                        color_continuous_scale=px.colors.sequential.Greens,
                        title="Soma de Lucro (Profit)")
    st.plotly_chart(fig2, use_container_width=True)

# Linha 3: Gráfico de Pizza
st.subheader("Visual de Pizza: Lucro por Segmento")
fig3 = px.pie(df_selection, values='Profit', names='Segment', 
             hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig3, use_container_width=True)
