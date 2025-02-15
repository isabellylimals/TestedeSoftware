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


def test_chamar_proximo(capsys):
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    # Primeiro, registra um paciente e um atendimento
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()

    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
        cli.registrar_atendimento()

    # Chama o próximo da fila
    cli.chamar_proximo()

    # Verifica a saída impressa no terminal
    captured = capsys.readouterr()
    assert "Próximo Paciente" in captured.out


def test_buscar_historico(capsys):
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    # Primeiro, registra um paciente e um atendimento
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()

    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
        cli.registrar_atendimento()

    # Busca o histórico
    with patch('builtins.input', side_effect=["12345678900"]):
        cli.buscar_historico()

    # Verifica a saída impressa no terminal
    captured = capsys.readouterr()
    assert "Histórico de atendimentos para João Silva" in captured.out