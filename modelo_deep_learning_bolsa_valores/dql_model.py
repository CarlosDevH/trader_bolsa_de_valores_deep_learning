import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd

print("foi")
class DQLModel(nn.Module):
    def __init__(self, n_features, n_actions):
        super(DQLModel, self).__init__()
        self.fc1 = nn.Linear(n_features, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, n_actions)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

def calcular_recompensa(acao, preco_atual, preco_futuro):
    """
    Calcula a recompensa baseada em dados reais.
    """
    if acao == 1:  # Comprar
        return preco_futuro - preco_atual  # Lucro se o preço subir
    elif acao == 2:  # Vender
        return preco_atual - preco_futuro  # Lucro se o preço cair
    else:  # Manter
        return -0.1  # Penalidade leve por manter

def treinar_modelo(df, modelo, n_episodios=1, epsilon=1.0, gamma=0.99, epsilon_min=0.1, epsilon_decay=0.995):
    """
    Treina o modelo de aprendizado por reforço usando DQL.
    """
    # Certifique-se de que o DataFrame contém apenas valores numéricos
    df = df[['close', 'SMA_20', 'RSI']].dropna()
    df = df.astype(float)  # Garante que os dados sejam float

    optimizer = optim.Adam(modelo.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    recompensas = []

    for episodio in range(n_episodios):
        print(f"Iniciando episódio {episodio + 1}/{n_episodios}...")
        total_recompensa = 0

        for passo in range(len(df) - 1):
            estado_atual = torch.tensor(df.iloc[passo].values, dtype=torch.float32).unsqueeze(0)
            preco_atual = df.iloc[passo]['close']
            preco_futuro = df.iloc[passo + 1]['close']

            # Escolher ação
            if torch.rand(1).item() < epsilon:
                acao = torch.randint(0, 3, (1,)).item()
            else:
                acao = torch.argmax(modelo(estado_atual)).item()

            recompensa = calcular_recompensa(acao, preco_atual, preco_futuro)

            # Atualizar a função Q
            estado_proximo = torch.tensor(df.iloc[passo + 1].values, dtype=torch.float32).unsqueeze(0)
            alvo = modelo(estado_atual).detach()
            alvo[0, acao] = recompensa + gamma * torch.max(modelo(estado_proximo))
            loss = criterion(modelo(estado_atual), alvo)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_recompensa += recompensa

        recompensas.append(total_recompensa)
        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        print(f"Episódio {episodio + 1} concluído. Recompensa total: {total_recompensa:.2f}")

    pd.DataFrame(recompensas, columns=['recompensa']).to_csv("logs/recompensas.csv", index=False)
    torch.save(modelo.state_dict(), "model/modelo_dql.pth")
    print("Modelo treinado e salvo com sucesso!")
