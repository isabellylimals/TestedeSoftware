# tests/test_service.py

import pytest
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository
from main.domain import Paciente, FichaAnalise

def test_registrar_paciente():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    assert paciente.nome == "João Silva"
    assert paciente.cpf == "12345678900"

def test_classificar_risco():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=True, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    assert risco.name == "Emergência"

def test_chamar_proximo_sem_pacientes():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    with pytest.raises(Exception) as exc_info:
        service.chamar_proximo()
    assert str(exc_info.value) == "Não há pacientes na fila"