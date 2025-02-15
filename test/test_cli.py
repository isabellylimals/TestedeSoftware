# tests/test_cli.py

import pytest
from unittest.mock import patch
from main.cli import TerminalClient
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository

def test_registrar_paciente_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)
    
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.nome == "João Silva"
    assert paciente.cpf == "12345678900"