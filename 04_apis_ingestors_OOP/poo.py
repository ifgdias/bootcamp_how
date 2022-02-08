import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} e tem {self.idade} anos"


israel = Pessoa(nome='Israel', sobrenome='Dias', data_de_nascimento=datetime.date(1985,9,14))

print(israel.nome, israel.sobrenome, israel.data_de_nascimento)

print(israel.idade)

print(israel)