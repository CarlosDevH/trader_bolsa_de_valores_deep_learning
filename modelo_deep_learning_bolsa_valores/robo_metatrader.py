import MetaTrader5 as mt5

def executar_operacao(acao, ativo, volume=0.1):
    """
    Executa operações de compra, venda ou manutenção no MetaTrader 5.
    """
    if not mt5.initialize():
        print("Erro ao inicializar o MetaTrader 5")
        return False

    # Validar informações do ativo
    info = mt5.symbol_info(ativo)
    if info is None:
        print(f"Ativo {ativo} não encontrado!")
        mt5.shutdown()
        return False

    if not info.visible:
        print(f"Ativo {ativo} está oculto. Tentando ativar...")
        if not mt5.symbol_select(ativo, True):
            print(f"Erro ao ativar o ativo {ativo}.")
            mt5.shutdown()
            return False

    # Obter o preço atual do ativo
    tick = mt5.symbol_info_tick(ativo)
    if tick is None:
        print(f"Erro ao obter o preço do ativo {ativo}")
        mt5.shutdown()
        return False

    # Configurar ordem
    if acao == 1:  # Comprar
        ordem = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": ativo,
            "volume": volume,
            "type": 0,  # 0 para ordem de compra
            "price": tick.ask,
            "deviation": 10,
            "magic": 234000,  # ID único para identificar a ordem
            "comment": "Ordem de compra automatizada",
        }
    elif acao == 2:  # Vender
        ordem = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": ativo,
            "volume": volume,
            "type": 1,  # 1 para ordem de venda
            "price": tick.bid,
            "deviation": 10,
            "magic": 234000,  # ID único para identificar a ordem
            "comment": "Ordem de venda automatizada",
        }
    else:
        print("Ação inválida! Use 1 (Comprar) ou 2 (Vender).")
        mt5.shutdown()
        return False

    # Enviar ordem
    resultado = mt5.order_send(ordem)
    if resultado.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Erro ao executar operação: {resultado.retcode}")
        mt5.shutdown()
        return False

    print(f"Operação executada com sucesso: {resultado}")
    mt5.shutdown()
    return True

if __name__ == "__main__":
    # Teste básico
    ativo = "PETR4"
    executar_operacao(acao=1, ativo=ativo)
