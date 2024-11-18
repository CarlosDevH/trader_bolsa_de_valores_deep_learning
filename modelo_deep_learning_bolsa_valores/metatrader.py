import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def coletar_dados(ativo, timeframe, inicio=None, fim=None):
    """
    Coleta dados históricos ou em tempo real do MetaTrader 5.
    """
    # Inicializa o MetaTrader 5
    if not mt5.initialize():
        print("Erro ao inicializar o MetaTrader 5")
        return None

    # Coleta dados históricos
    if inicio and fim:
        dados = mt5.copy_rates_range(ativo, timeframe, inicio, fim)
    else:
        # Coleta dados em tempo real
        dados = mt5.copy_rates_from_pos(ativo, timeframe, 0, 100)

    mt5.shutdown()

    if dados is None or len(dados) == 0:
        print(f"Erro ao obter dados do ativo {ativo}")
        return None

    # Converter para DataFrame
    df = pd.DataFrame(dados)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Converter timestamps para datetime
    return df

if __name__ == "__main__":
    ativo = "PETR4"
    timeframe = mt5.TIMEFRAME_H1
    inicio = datetime(2024, 1, 1)
    fim = datetime(2024, 11, 17)

    df = coletar_dados(ativo, timeframe, inicio, fim)
    if df is not None:
        df.to_csv("data/dados_historicos.csv", index=False)
        print("Dados coletados com sucesso!")
