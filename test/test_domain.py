import pytest
from datetime import datetime
from main.domain import (
    Paciente, Risco, FichaAnalise, Atendimento, FilaAtendimento,
    ValidacaoError, FilaVaziaError
)


def test_paciente_valido():
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    assert paciente.nome == "João Silva"
    assert paciente.cpf == "12345678901"
    assert paciente.email == "joao@example.com"

def test_paciente_nome_invalido():
    with pytest.raises(ValidacaoError):
        Paciente(nome="123", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")

def test_paciente_cpf_invalido():
    with pytest.raises(ValidacaoError):
        Paciente(nome="João Silva", cpf="123", email="joao@example.com", nascimento="01/01/1990")

def test_paciente_email_invalido():
    with pytest.raises(ValidacaoError):
        Paciente(nome="João Silva", cpf="12345678901", email="joao", nascimento="01/01/1990")

def test_paciente_nascimento_invalido():
    with pytest.raises(ValidacaoError):
        Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="31/02/1990") 

def test_paciente_nascimento_futuro():
    with pytest.raises(ValidacaoError):
        Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/2100")  


def test_risco_valores():
    assert Risco.VERMELHO.value == 1
    assert Risco.LARANJA.value == 2
    assert Risco.AMARELO.value == 3
    assert Risco.VERDE.value == 4
    assert Risco.AZUL.value == 5


def test_ficha_analise():
    ficha = FichaAnalise(risco_morte=True, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    assert ficha.risco_morte is True
    assert ficha.gravidade_alta is True
    assert ficha.gravidade_moderada is False
    assert ficha.gravidade_baixa is False

def test_atendimento_valido():
    paciente = Paciente(nome="Maria", cpf="98765432100", email="maria@example.com", nascimento="15/05/1985")
    atendimento = Atendimento(paciente=paciente, risco=Risco.VERMELHO)
    assert atendimento.paciente.nome == "Maria"
    assert atendimento.risco == Risco.VERMELHO
    assert isinstance(atendimento.entrada, datetime)

def test_atendimento_paciente_invalido():
    with pytest.raises(ValidacaoError):
        paciente = Paciente(nome="Maria", cpf="98765432100", email="maria@example.com", nascimento="31/02/1985") 
        Atendimento(paciente=paciente, risco=Risco.VERMELHO)


def test_fila_atendimento_inserir_e_proximo():
    fila = FilaAtendimento()
    paciente1 = Paciente(nome="João", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    paciente2 = Paciente(nome="Maria", cpf="98765432100", email="maria@example.com", nascimento="15/05/1985")

    atendimento1 = Atendimento(paciente=paciente1, risco=Risco.VERDE)
    atendimento2 = Atendimento(paciente=paciente2, risco=Risco.VERMELHO)

    fila.inserir(atendimento1)
    fila.inserir(atendimento2)

    assert fila.proximo().paciente.nome == "Maria"  
    assert fila.proximo().paciente.nome == "João"

def test_fila_atendimento_vazia():
    fila = FilaAtendimento()
    with pytest.raises(FilaVaziaError):
        fila.proximo()

def test_fila_atendimento_inserir_invalido():
    fila = FilaAtendimento()
    with pytest.raises(ValidacaoError):
        paciente = Paciente(nome="João", cpf="123", email="joao@example.com", nascimento="01/01/1990") 
        atendimento = Atendimento(paciente=paciente, risco=Risco.VERDE)
        fila.inserir(atendimento)