import datetime
import math
from typing import List


class Pessoa:
    def __init__(
        self,
        nome: str,
        sobrenome: str,
        data_de_nascimento: datetime.date):

        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome


    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} e tem {self.idade} anos"

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.experiencias = experiencias
        self.pessoa = pessoa

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)

    @property
    def cargo_atual(self) -> str:
        return self.experiencias[-1]

    def adiciona_experiencia(self, experiencia: str):
        self.experiencias.append(experiencia)

    def __str__(self) -> str:
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} e já " \
            f"trabalhou em {self.quantidade_de_experiencias} empresas, sendo que " \
                f"atualmente trabalha na empresa {self.cargo_atual}."


israel = Pessoa(nome='Israel', sobrenome='Dias', data_de_nascimento=datetime.date(1985,9,14))

curriculo_israel = Curriculo(
    pessoa=israel,
    experiencias=['IMC','ZOPONE','CONSTRUCAP']
)

print(israel)

print(curriculo_israel)