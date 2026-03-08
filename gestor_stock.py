# gestor_stock.py

class GestorStock:
    """Classe que representa um gestor de carteira de uma ação específica."""

    def __init__(self, simbolo: str, nome: str, preco_atual=0.0, quantidade=0):
        pass

    @property
    def simbolo(self) -> str:
        """Devolve o símbolo da ação (ex: AAPL).
        O símbolo deve ser guardado e devolvido sem espaços adicionais e em maiúsculas."""
        pass

    @simbolo.setter
    def simbolo(self, valor: str):
        """Define o símbolo da ação."""
        pass

    @property
    def nome(self) -> str:
        """Devolve o nome da empresa.
        O nome deve ser guardado e devolvido sem espaços adicionais e com as iniciais em maiúsculas (Title Case)."""
        pass

    @nome.setter
    def nome(self, valor: str):
        """Define o nome da empresa."""
        pass

    @property
    def preco_atual(self) -> float:
        """Devolve o preço atual da ação."""
        pass

    @preco_atual.setter
    def preco_atual(self, valor: float):
        """Define o preço atual da ação. Deve ser positivo.
        Se for fornecido um valor negativo ou zero, o preço é colocado a 0."""
        pass

    @property
    def quantidade(self) -> int:
        """Devolve a quantidade de ações em carteira."""
        pass

    @quantidade.setter
    def quantidade(self, valor: int):
        """Define a quantidade de ações em carteira.
        Se for fornecido um valor negativo, a quantidade é colocada a 0."""
        pass

    @property
    def preco_medio_compra(self) -> float:
        """Devolve o preço médio de compra vigente de todo o stock."""
        pass

    @preco_medio_compra.setter
    def preco_medio_compra(self, valor: float):
        """Define o preço médio de compra."""
        pass

    @property
    def lucro_realizado(self) -> float:
        """Devolve o lucro (ou prejuízo) consolidado ao longo de todo o histórico de transações de venda e dividendos fechados."""
        pass

    @lucro_realizado.setter
    def lucro_realizado(self, valor: float):
        """Define o lucro realizado."""
        pass

    def comprar(self, quantidade: int, preco: float) -> bool:
        """Realiza uma compra de ações.
        Aumenta a quantidade em carteira, estipula o novo preço médio de compra através da média pesada, e atualiza o preço de mercado atual.
        Retorna True no sucesso e False no caso de inputs (quantidade ou preco) não serem > 0."""
        pass

    def vender(self, quantidade: int, preco: float) -> bool:
        """Realiza uma venda de ações.
        Diminui a quantidade em carteira, atualiza o preço atual, e soma a margem (lucro ou prejuízo) face ao preço_medio_compra ao histórico de lucro_realizado.
        Retorna True no sucesso e False no insucesso (seja por parâmetros errados <= 0 ou pela inexistência de posições suficientes)."""
        pass

    def valor_total(self) -> float:
        """Calcula o valor total da posição na carteira (quantidade * preço_atual)."""
        pass

    def lucro_potencial(self) -> float:
        """Apurar rentabilidade não realizada ao valor de cotação presente.
        Diferença entre a avaliação do ativo aos preços de hoje, e a avaliação ao preço que foi comprado."""
        pass

    def receber_dividendo(self, dividendo_por_acao: float) -> float:
        """Apurar dividendos totais com o número de ações em posse, adicionando diretamente ao lucro_realizado da posição.
        Retorna o fundo depositado (que será 0.0 se for passado um valor inválido <= 0)."""
        pass
