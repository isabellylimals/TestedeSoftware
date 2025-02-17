import pytest
from main.cli import TerminalClient
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository

def test_registrar_paciente_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    # Simula a entrada do usuário
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    paciente = paciente_repo.buscar("12345678900")
    assert paciente.nome == "João Silva"
    assert paciente.cpf == "12345678900"

def test_registrar_atendimento_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    # Registra um paciente
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    # Registra um atendimento
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "sim")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        cli.registrar_atendimento()

    paciente = paciente_repo.buscar("12345678900")
    assert len(service.buscar_historico(paciente)) == 1

def test_chamar_proximo(capsys):
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    # Registra um paciente
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    # Registra um atendimento
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "sim")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
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

    # Registra um paciente
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    # Registra um atendimento
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "sim")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        cli.registrar_atendimento()

    # Busca o histórico
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        cli.buscar_historico()

    # Verifica a saída impressa no terminal
    captured = capsys.readouterr()
    assert "Histórico de atendimentos para João Silva" in captured.out