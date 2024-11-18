
import MetaTrader5 as mt5
from datetime import datetime
from metatrader import coletar_dados
from process_data import adicionar_indicadores
from dql_model import DQLModel, treinar_modelo
from robo_metatrader import executar_operacao
import pandas as pd
import torch

# Configuração inicial
ativo = "PETR4"
timeframe = mt5.TIMEFRAME_H1
inicio = datetime(2023, 1, 1)
fim = datetime(2024, 11, 17)
n_episodios = 200  # Aumente conforme necessário
n_features = 3
n_actions = 3

# Etapa 1: Coletar dados do MetaTrader
print("Coletando dados do MetaTrader...")
dados = coletar_dados(ativo=ativo, timeframe=timeframe, inicio=inicio, fim=fim)

if dados is not None:
    dados.to_csv("data/dados_historicos.csv", index=False)
    print("Dados coletados com sucesso!")

    print("Verificando os dados coletados:")
    print(dados.head())
    print("Colunas dos dados coletados:", dados.columns)

    # Etapa 2: Adicionar indicadores
    adicionar_indicadores("data/dados_historicos.csv")
    df = pd.read_csv("data/dados_processados.csv").dropna()

    # Etapa 3: Criar e treinar o modelo
    modelo = DQLModel(n_features=n_features, n_actions=n_actions)
    treinar_modelo(df, modelo, n_episodios=n_episodios)

    # Etapa 4: Usar modelo treinado
    modelo.load_state_dict(torch.load("model/modelo_dql.pth"))
    modelo.eval()
    print("Modelo carregado para execução!")

    # Decisão com base em dados em tempo real
    # Decisão com base em dados em tempo real
    # Carregar dados já processados para simulação
    df_realtime = pd.read_csv("data/dados_processados.csv").dropna()

    if not df_realtime.empty:
        estado = torch.tensor(df_realtime[['close', 'SMA_20', 'RSI']].iloc[-1].values, dtype=torch.float32).unsqueeze(0)
        acao = torch.argmax(modelo(estado)).item()
        acoes = ["Manter", "Comprar", "Vender"]
        print(f"Ação recomendada: {acoes[acao]}")
        executar_operacao(acao, ativo)
    else:
        print("Erro: Arquivo 'dados_processados.csv' está vazio ou ausente.")
