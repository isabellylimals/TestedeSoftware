import pytest
from main.domain import Paciente, Atendimento
from main.repository import PacienteRepository, AtendimentoRepository
from main.error import CPFDuplicadoError, PacienteNaoCadastradoError

def test_inserir_paciente():
    repo = PacienteRepository()
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    repo.inserir(paciente)
    assert len(repo.pacientes) == 1
    assert repo.pacientes[0] == paciente

def test_buscar_paciente_existente():
    repo = PacienteRepository()
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    repo.inserir(paciente)
    resultado = repo.buscar("12345678901")
    assert resultado == paciente

def test_buscar_paciente_inexistente():
    repo = PacienteRepository()
    resultado = repo.buscar("12345678901")
    assert resultado is None

def test_inserir_atendimento_paciente_cadastrado():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    paciente_repo.inserir(paciente)
    atendimento = Atendimento(paciente=paciente, risco="VERMELHO")
    atendimento_repo.inserir(atendimento)
    assert len(atendimento_repo.atendimentos) == 1
    assert atendimento_repo.atendimentos[0] == atendimento

def test_inserir_atendimento_paciente_nao_cadastrado():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    atendimento = Atendimento(paciente=paciente, risco="VERMELHO")
    with pytest.raises(PacienteNaoCadastradoError):
        atendimento_repo.inserir(atendimento)

def test_historico_atendimentos_paciente_cadastrado():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    paciente = Paciente(nome="João Silva", cpf="12345678901", email="joao@example.com", nascimento="01/01/1990")
    paciente_repo.inserir(paciente)
    atendimento1 = Atendimento(paciente=paciente, risco="VERMELHO")
    atendimento2 = Atendimento(paciente=paciente, risco="LARANJA")
    atendimento_repo.inserir(atendimento1)
    atendimento_repo.inserir(atendimento2)
    historico = atendimento_repo.historico_atendimentos("12345678901")
    assert len(historico) == 2
    assert historico[0] == atendimento1
    assert historico[1] == atendimento2

def test_historico_atendimentos_paciente_nao_cadastrado():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    with pytest.raises(PacienteNaoCadastradoError):
        atendimento_repo.historico_atendimentos("12345678901")