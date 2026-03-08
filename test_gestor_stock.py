# test_gestor_stock.py
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pytest",
# ]
# ///
import pytest
from gestor_stock import GestorStock

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

if __name__ == "__main__":
    # Permite executar o teste diretamente com `uv run test_gestor_stock.py`
    import sys
    from pytest import main
    sys.exit(main(["-v", __file__]))
