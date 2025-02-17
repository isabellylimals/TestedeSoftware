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

def test_registrar_paciente_cpf_duplicado():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente1 = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    with pytest.raises(Exception) as exc_info:
        service.registrar_paciente("Maria Silva", "12345678900", "maria@example.com", "02/02/1990")
    assert "CPF já cadastrado" in str(exc_info.value)

def test_classificar_risco_vermelho():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=True, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    assert risco.name == "VERMELHO"

def test_classificar_risco_amarelo():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    assert risco.name == "AMARELO"

def test_classificar_risco_laranja():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=True, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    assert risco.name == "LARANJA"

def test_classificar_risco_verde():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=True)
    risco = service.classificar_risco(ficha)
    assert risco.name == "VERDE"

def test_classificar_risco_azul():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=False, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    assert risco.name == "AZUL"

def test_registrar_atendimento():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    
    atendimento = service.registrar_atendimento(paciente, risco)
    assert atendimento.paciente.cpf == "12345678900"
    assert atendimento.risco.name == "AMARELO"

def test_inserir_fila_atendimento():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    atendimento = service.registrar_atendimento(paciente, risco)
    
    resultado = service.inserir_fila_atendimento(atendimento)
    assert resultado is True

def test_chamar_proximo_sem_pacientes():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    with pytest.raises(Exception) as exc_info:
        service.chamar_proximo()
    assert str(exc_info.value) == "Não há pacientes na fila"

def test_chamar_proximo_com_pacientes():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    atendimento = service.registrar_atendimento(paciente, risco)
    service.inserir_fila_atendimento(atendimento)
    
    proximo = service.chamar_proximo()
    assert proximo.paciente.nome == "João Silva"

def test_buscar_historico_vazio():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    historico = service.buscar_historico(paciente)
    assert len(historico) == 0

def test_buscar_historico_com_atendimentos():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    
    paciente = service.registrar_paciente("João Silva", "12345678900", "joao@example.com", "01/01/1990")
    ficha = FichaAnalise(risco_morte=False, gravidade_alta=True, gravidade_moderada=False, gravidade_baixa=False)
    risco = service.classificar_risco(ficha)
    atendimento = service.registrar_atendimento(paciente, risco)
    service.inserir_fila_atendimento(atendimento)
    
    historico = service.buscar_historico(paciente)
    assert len(historico) == 1
    assert historico[0].paciente.nome == "João Silva"