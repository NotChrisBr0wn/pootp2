# test_gestor_stock.py
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
# ]
# ///
import pytest
from gestor_stock import GestorStock, Carteira

@pytest.fixture
def gestor():
    return GestorStock(" aAPL  ", " aPPLe iNc. ", 150.0, 10)

def test_inicializacao(gestor):
    assert gestor.simbolo == "AAPL"
    assert gestor.nome == "Apple Inc."
    assert gestor.preco_atual == 150.0
    assert gestor.quantidade == 10
    assert gestor.preco_medio_compra == 150.0
    assert gestor.lucro_realizado == 0.0

def test_valor_total(gestor):
    assert gestor.valor_total() == 1500.0

def test_comprar(gestor):
    sucesso = gestor.comprar(5, 180.0)
    assert sucesso is True
    assert gestor.quantidade == 15
    assert gestor.preco_atual == 180.0
    # Media pesada: (150*10 + 180*5) / 15 = 160.0
    assert gestor.preco_medio_compra == 160.0

def test_vender_lucro(gestor):
    # Comprou 10 a 150. Vende 5 a 170.
    sucesso = gestor.vender(5, 170.0)
    assert sucesso is True
    assert gestor.quantidade == 5
    assert gestor.preco_atual == 170.0
    # Lucro = (170 - 150) * 5 = 100
    assert gestor.lucro_realizado == 100.0

def test_vender_prejuizo(gestor):
    # Comprou 10 a 150. Vende 5 a 100.
    sucesso = gestor.vender(5, 100.0)
    assert sucesso is True
    assert gestor.quantidade == 5
    assert gestor.preco_atual == 100.0
    # Prejuizo = (100 - 150) * 5 = -250
    assert gestor.lucro_realizado == -250.0

def test_vender_insuficiente(gestor):
    sucesso = gestor.vender(20, 170.0)
    assert sucesso is False
    assert gestor.quantidade == 10
    assert gestor.lucro_realizado == 0.0

def test_validacao_preco(gestor):
    gestor.preco_atual = -10
    assert gestor.preco_atual == 0.0

def test_validacao_quantidade(gestor):
    gestor.quantidade = -5
    assert gestor.quantidade == 0

def test_validacao_string_strip():
    g = GestorStock("  msft  ", "   microsoft corp. \n", 10, 1)
    assert g.simbolo == "MSFT"
    assert g.nome == "Microsoft Corp."

def test_comprar_invalido(gestor):
    sucesso = gestor.comprar(-5, 160.0)
    assert sucesso is False

    sucesso = gestor.comprar(5, -10.0)
    assert sucesso is False

    assert gestor.quantidade == 10
    assert gestor.preco_medio_compra == 150.0

def test_vender_invalido(gestor):
    sucesso = gestor.vender(-5, 160.0)
    assert sucesso is False

    sucesso = gestor.vender(5, -10.0)
    assert sucesso is False

    assert gestor.quantidade == 10
    assert gestor.lucro_realizado == 0.0

def test_lucro_potencial(gestor):
    # preco comprado a 150. cotacao de mercado sobe pra 200.
    gestor.preco_atual = 200.0
    assert gestor.lucro_potencial() == 500.0  # (200-150) * 10

def test_receber_dividendo(gestor):
    # ganha 2.5 euros por cada acao
    montante = gestor.receber_dividendo(2.5)
    assert montante == 25.0
    assert gestor.lucro_realizado == 25.0

def test_receber_dividendo_invalido(gestor):
    montante = gestor.receber_dividendo(-2.5)
    assert montante == 0.0
    assert gestor.lucro_realizado == 0.0

def test_save_json(tmp_path, gestor):
    gestor.comprar(5, 180.0)
    gestor.vender(3, 200.0)

    caminho = tmp_path / "gestor.json"
    gestor.save(str(caminho))

    assert caminho.exists()

    carregado = GestorStock.load(str(caminho))
    assert carregado.simbolo == gestor.simbolo
    assert carregado.nome == gestor.nome
    assert carregado.preco_atual == gestor.preco_atual
    assert carregado.quantidade == gestor.quantidade
    assert carregado.preco_medio_compra == gestor.preco_medio_compra
    assert carregado.lucro_realizado == gestor.lucro_realizado
    assert carregado.historico_transacoes == gestor.historico_transacoes

def test_load_historico_invalido(tmp_path):
    caminho = tmp_path / "gestor_invalido.json"
    caminho.write_text(
        '{"simbolo":"AAPL","nome":"Apple Inc.","preco_atual":120.0,'
        '"quantidade":5,"lucro_realizado":10.0,"preco_medio_compra":100.0,'
        '"historico_transacoes":"invalido"}',
        encoding="utf-8",
    )

    gestor = GestorStock.load(str(caminho))
    assert gestor.historico_transacoes == []
    assert gestor.quantidade == 5
    assert gestor.preco_medio_compra == 100.0

def test_definir_preco_alvo_valido(gestor):
    sucesso = gestor.definir_preco_alvo(175.5)
    assert sucesso is True
    assert gestor.preco_alvo == 175.5

def test_definir_preco_alvo_invalido(gestor):
    sucesso = gestor.definir_preco_alvo(-1)
    assert sucesso is False
    assert gestor.preco_alvo is None

def test_verificar_alerta(gestor):
    gestor.definir_preco_alvo(160.0)
    assert gestor.verificar_alerta(159.99) is False
    assert gestor.verificar_alerta(160.0) is True
    assert gestor.verificar_alerta(200.0) is True
    assert gestor.verificar_alerta(-10.0) is False

def test_carteira_adicionar_e_remover():
    carteira = Carteira()
    apple = GestorStock("AAPL", "Apple Inc.", 150.0, 10)

    assert carteira.adicionar_acao(apple) is True
    assert carteira.adicionar_acao(apple) is False
    assert len(carteira.acoes) == 1

    assert carteira.remover_acao("aapl") is True
    assert carteira.remover_acao("AAPL") is False

def test_carteira_valor_total_e_lucro_global():
    carteira = Carteira()

    aapl = GestorStock("AAPL", "Apple Inc.", 150.0, 10)
    msft = GestorStock("MSFT", "Microsoft Corp.", 100.0, 20)

    # Ajusta o preço de mercado para gerar lucro/prejuízo potencial.
    aapl.preco_atual = 170.0  # potencial: (170-150)*10 = 200
    msft.preco_atual = 90.0   # potencial: (90-100)*20 = -200
    msft.vender(5, 110.0)     # realizado: (110-100)*5 = 50

    carteira.adicionar_acao(aapl)
    carteira.adicionar_acao(msft)

    assert carteira.valor_total() == 1700.0 + (15 * 110.0)
    assert carteira.lucro_global() == 200.0 + 200.0

# teste para verificar o metodo str (representação textual)
def test_str_representacao(gestor):
    texto = str(gestor)
    assert "AAPL" in texto
    assert "Apple Inc." in texto
    assert "Preço Atual: 150.00" in texto
    assert "Quantidade: 10" in texto
    assert "Valor Total: 1500.00" in texto
    assert "Lucro/Prejuízo: 0.00" in texto

if __name__ == "__main__":
    # Permite executar o teste diretamente com `uv run test_gestor_stock.py`
    import sys
    from pytest import main
    sys.exit(main(["-v", __file__]))
