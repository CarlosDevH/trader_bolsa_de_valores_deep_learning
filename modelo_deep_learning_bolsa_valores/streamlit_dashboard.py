import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Acompanhamento do Modelo de Trading com DQL")

# Carregar logs de recompensas
try:
    recompensas = pd.read_csv("logs/recompensas.csv")['recompensa']
except FileNotFoundError:
    st.error("Arquivo logs/recompensas.csv não encontrado. Treine o modelo primeiro!")
    recompensas = None

if recompensas is not None:
    # Gráfico de recompensas
    st.subheader("Recompensas por Episódio")
    fig, ax = plt.subplots()
    ax.plot(recompensas)
    ax.set_xlabel("Episódio")
    ax.set_ylabel("Recompensa Total")
    st.pyplot(fig)
