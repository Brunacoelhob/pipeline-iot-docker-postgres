# ===========================================================================
# PROJETO: Dashboard de Monitoramento IoT
# VERSÃO: 1.0
# AUTOR: Bruna Coelho
# DATA: 15/04/2026
# OBJETIVO: 
# Visualização interativa dos dados de temperatura processados,
# utilizando Streamlit e consultas SQL em tempo real.
# ==========================================================================

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="IoT Temperature Dashboard", layout="wide")

# Conexão com o banco (Mesmas credenciais do main.py)
engine = create_engine('postgresql://bruna:adminadmin@127.0.0.1:5432/iot_db')

def load_data():
    """Busca os dados diretamente do PostgreSQL."""
    query = "SELECT * FROM temperature_readings ORDER BY noted_date DESC"
    return pd.read_sql(query, engine)

def main():
    st.title("🌡️ Monitoramento de Sensores IoT")
    st.markdown("---")

    # Carregando os dados
    try:
        df = load_data()
        
        # --- LADO A LADO: Métricas Principais ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Leituras", len(df))
        with col2:
            st.metric("Temp. Média", f"{df['temp'].mean():.2f}°C")
        with col3:
            st.metric("Sensores Ativos", df['id'].nunique())

        st.markdown("---")

        # --- GRÁFICO: Evolução da Temperatura ---
        st.subheader("Linha do Tempo de Temperatura")
        fig_line = px.line(df, x='noted_date', y='temp', color='out/in',
                          title="Variação de Temperatura (Interno vs Externo)")
        st.plotly_chart(fig_line, use_container_width=True)

        # --- TABELA: Dados Brutos ---
        st.subheader("Últimas Leituras do Banco")
        st.dataframe(df.head(50), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao carregar dados do banco: {e}")
        st.info("Certifique-se de que o Docker está rodando e o script main.py foi executado.")

if __name__ == "__main__":
    main()