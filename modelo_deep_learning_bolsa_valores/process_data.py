import pandas as pd

def adicionar_indicadores(data):
    # Se for uma string, carregue como CSV. Caso contrário, considere que já é um DataFrame.
    if isinstance(data, str):
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise ValueError("O argumento deve ser um caminho para um arquivo CSV ou um DataFrame.")

    # Adicionar indicadores técnicos
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    delta = df['close'].diff()
    ganhos = delta.where(delta > 0, 0)
    perdas = -delta.where(delta < 0, 0)
    media_ganhos = ganhos.rolling(window=14).mean()
    media_perdas = perdas.rolling(window=14).mean()
    rs = media_ganhos / media_perdas
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

