# gestor_stock.py

class GestorStock:
    def __init__(self, simbolo: str, nome: str, preco_atual=0.0, quantidade=0):
        self.simbolo = simbolo
        self.nome = nome
        self.preco_atual = preco_atual
        self.quantidade = quantidade

        self.lucro_realizado = 0.0
        self.preco_medio_compra = float(preco_atual) if quantidade > 0 else 0.0
        

    @property
    def simbolo(self) -> str:
        return self._simbolo

    @simbolo.setter
    def simbolo(self, valor: str):
        self._simbolo = valor.strip().upper()

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        self._nome = valor.strip().title()

    @property
    def preco_atual(self) -> float:
        """Devolve o preço atual da ação."""
        return self._preco_atual

    @preco_atual.setter
    def preco_atual(self, valor: float):
        """Define o preço atual da ação. Deve ser positivo.
        Se for fornecido um valor negativo ou zero, o preço é colocado a 0."""
        if valor > 0:
            self._preco_atual = float(valor)
        else:
            self._preco_atual = 0.0

    @property
    def quantidade(self) -> int:
        """Devolve a quantidade de ações em carteira."""
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int):
        """Define a quantidade de ações em carteira.
        Se for fornecido um valor negativo, a quantidade é colocada a 0."""
        if valor >= 0:
            self._quantidade = int(valor)
        else:
            self._quantidade = 0

    @property
    def preco_medio_compra(self) -> float:
        """Devolve o preço médio de compra vigente de todo o stock."""
        return self._preco_medio_compra

    @preco_medio_compra.setter
    def preco_medio_compra(self, valor: float):
        """Define o preço médio de compra."""
        self._preco_medio_compra = float(valor)

    @property
    def lucro_realizado(self) -> float:
        """Devolve o lucro (ou prejuízo) consolidado ao longo de todo o histórico de transações de venda e dividendos fechados."""
        return self._lucro_realizado

    @lucro_realizado.setter
    def lucro_realizado(self, valor: float):
        """Define o lucro realizado."""
        self._lucro_realizado = float(valor)

    def comprar(self, quantidade: int, preco: float) -> bool:
        """Realiza uma compra de ações.
        Aumenta a quantidade em carteira, estipula o novo preço médio de compra através da média pesada, e atualiza o preço de mercado atual.
        Retorna True no sucesso e False no caso de inputs (quantidade ou preco) não serem > 0."""
        if quantidade <= 0 or preco <= 0:
            return False
        
        custo_total_anterior = self.preco_medio_compra * self.quantidade
        custo_total_novo = preco * quantidade

        nova_quantidade = self.quantidade + quantidade

        self.preco_medio_compra = (custo_total_anterior + custo_total_novo) / (nova_quantidade)

        self.quantidade = nova_quantidade
        self.preco_atual = preco
        return True

    def vender(self, quantidade: int, preco: float) -> bool:
        """Realiza uma venda de ações.
        Diminui a quantidade em carteira, atualiza o preço atual, e soma a margem (lucro ou prejuízo) face ao preço_medio_compra ao histórico de lucro_realizado.
        Retorna True no sucesso e False no insucesso (seja por parâmetros errados <= 0 ou pela inexistência de posições suficientes)."""
        pass

    def valor_total(self) -> float:
        """Calcula o valor total da posição na carteira (quantidade * preço_atual)."""
        return self.quantidade * self.preco_atual

    def lucro_potencial(self) -> float:
        """Apurar rentabilidade não realizada ao valor de cotação presente.
        Diferença entre a avaliação do ativo aos preços de hoje, e a avaliação ao preço que foi comprado."""
        pass

    def receber_dividendo(self, dividendo_por_acao: float) -> float:
        """Apurar dividendos totais com o número de ações em posse, adicionando diretamente ao lucro_realizado da posição.
        Retorna o fundo depositado (que será 0.0 se for passado um valor inválido <= 0)."""
        pass
