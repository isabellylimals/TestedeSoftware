# tests/test_cli.py

from unittest.mock import patch
from main.cli import TerminalClient
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository

def test_registrar_paciente_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)
    
    # Simula a entrada do usuário
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    
    # Verifica se o paciente foi registrado corretamente
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.nome == "João Silva"
    assert paciente.cpf == "12345678900"

def test_registrar_atendimento_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)
    
    # Primeiro, registra um paciente
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    
    # Simula a entrada do usuário para registrar um atendimento
    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
        cli.registrar_atendimento()
    
    # Verifica se o atendimento foi registrado corretamente
    paciente = paciente_repo.buscar("12345678900")
    assert len(service.buscar_historico(paciente)) == 1