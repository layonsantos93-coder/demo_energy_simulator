import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Configurações do app ---
st.set_page_config(page_title="Energy Monitoring", layout="wide", page_icon="⚡", initial_sidebar_state="expanded")

# --- Tema escuro e título ---
st.markdown("<h1 style='color:#00FF00; text-align:center;'>⚡ Energy Monitoring</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:lightgray;'>💡 Dashboard de monitoramento de energia limpa - demo interativo</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Dados fictícios ---
estados = ["SP", "RJ", "MG", "BA"]
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho"]
np.random.seed(42)

dados = []
for estado in estados:
    for mes in meses[:-1]:
        consumo = np.random.uniform(50, 250)
        gasto = min(consumo * np.random.uniform(0.8,0.9), 200)
        dados.append([mes, estado, consumo, gasto])

# Mês atual
mes_atual = meses[-1]

# --- Sidebar ---
st.sidebar.header("Configurações")
estado_sel = st.sidebar.selectbox("Selecione o estado:", estados)
consumo_atual = st.sidebar.number_input(f"Consumo de {mes_atual} (kWh):", min_value=0.0, step=1.0)
preco_kwh = np.random.uniform(0.8,0.9)
gasto_atual = min(consumo_atual * preco_kwh, 200)

if st.sidebar.button(f"Adicionar consumo de {mes_atual}"):
    dados.append([mes_atual, estado_sel, consumo_atual, gasto_atual])
    st.sidebar.success(f"✅ Registro adicionado! Gasto estimado: R$ {gasto_atual:.2f}")

# --- Criar DataFrame ---
df = pd.DataFrame(dados, columns=["Mês", "Estado", "Consumo (kWh)", "Gasto (R$)"])
df_estado = df[df["Estado"] == estado_sel]

# --- Cards resumidos ---
consumo_total = df_estado["Consumo (kWh)"].sum()
gasto_total = df_estado["Gasto (R$)"].sum()
consumo_medio = df_estado["Consumo (kWh)"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("⚡ Consumo total (kWh)", f"{consumo_total:.1f}")
col2.metric("💰 Gasto total (R$)", f"{gasto_total:.2f}")
col3.metric("📊 Consumo médio/mês (kWh)", f"{consumo_medio:.1f}")

st.markdown("---")

# --- Gráfico Gauge do mês atual ---
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=gasto_atual,
    delta={'reference': 200, 'increasing': {'color': "red"}},
    gauge={'axis': {'range': [0,200]},
           'bar': {'color': "green"},
           'steps': [
               {'range': [0,100], 'color': "lightgreen"},
               {'range': [100,200], 'color': "yellow"}]},
    title={'text': f"Gasto do mês atual ({mes_atual})"}
))
st.plotly_chart(fig_gauge, use_container_width=True)

# --- Gráfico de barras: Consumo por mês ---
st.subheader(f"📊 Consumo por mês - Estado {estado_sel}")
fig1 = px.bar(df_estado, x="Mês", y="Consumo (kWh)", text="Gasto (R$)",
              color="Mês", color_continuous_scale=px.colors.sequential.Teal,
              title="Consumo nos meses anteriores e atual")
fig1.update_layout(showlegend=False, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="lightgray")
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico de linha: Gasto mensal ---
st.subheader(f"💰 Comparativo de gasto - Estado {estado_sel}")
fig2 = px.line(df_estado, x="Mês", y="Gasto (R$)", markers=True, title="Gasto mensal estimado (R$)")
fig2.update_traces(line=dict(color="green", width=4))
fig2.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font_color="lightgray")
st.plotly_chart(fig2, use_container_width=True)

# --- Tabela com histórico ---
st.subheader("📋 Histórico completo")
st.dataframe(df_estado.reset_index(drop=True))
