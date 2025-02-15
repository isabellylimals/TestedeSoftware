# tests/test_cli.py
import pytest
from unittest.mock import patch
from main.cli import TerminalClient
from main.service import ProntoSocorroService
from main.repository import PacienteRepository, AtendimentoRepository
from main.error import PSBaseError

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



@pytest.fixture
def setup_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)
    return cli, paciente_repo, service

# CT1: NOME
def test_nome_valido(setup_cli):
    cli, paciente_repo, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.nome == "João Silva"

def test_nome_longo(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva da Costa e Oliveira", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Nome deve ter no máximo 10 caracteres." in captured.out

def test_nome_vazio(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Nome não informado ou contém apenas espaços." in captured.out

def test_nome_apenas_espacos(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["   ", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Nome não informado ou contém apenas espaços." in captured.out

def test_nome_invalido_caracteres(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João@Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Nome contém caracteres inválidos." in captured.out

# CT2: CPF
def test_cpf_valido(setup_cli):
    cli, paciente_repo, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.cpf == "12345678900"

def test_cpf_curto(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "123456789", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF deve ter exatamente 11 dígitos." in captured.out

def test_cpf_longo(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "123456789000", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF deve ter exatamente 11 dígitos." in captured.out

def test_cpf_vazio(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF não informado ou contém apenas espaços." in captured.out

def test_cpf_invalido_caracteres(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "123abc45678", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF deve conter apenas números." in captured.out


# CT3: E-MAIL
def test_email_valido(setup_cli):
    cli, paciente_repo, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.email == "joao@example.com"

def test_email_invalido_sem_arroba(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joaoexample.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "E-mail inválido." in captured.out

def test_email_vazio(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "E-mail não informado ou contém apenas espaços." in captured.out

def test_email_apenas_espacos(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "   ", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "E-mail não informado ou contém apenas espaços." in captured.out

# CT4: DATA DE NASCIMENTO
def test_data_valida(setup_cli):
    cli, paciente_repo, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    paciente = paciente_repo.buscar("12345678900")
    assert paciente.nascimento == "01/01/1990"

def test_data_invalida_dia(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "32/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Dia inválido." in captured.out

def test_data_invalida_mes(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/13/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Mês inválido." in captured.out

def test_data_invalida_ano(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/2026"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Ano inválido." in captured.out

def test_data_vazia(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", ""]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Data de nascimento não informada ou contém apenas espaços." in captured.out

def test_executar_sair(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', return_value="5"):  # Simula a opção de sair
        cli.executar()
    captured = capsys.readouterr()
    assert "Saindo do sistema..." in captured.out

def test_executar_opcao_invalida(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["6", "5"]):  # Opção inválida, depois sair
        cli.executar()
    captured = capsys.readouterr()
    assert "Opção inválida, tente novamente." in captured.out

def test_registrar_paciente_cpf_duplicado(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    with patch('builtins.input', side_effect=["Maria Silva", "12345678900", "maria@example.com", "02/02/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF já cadastrado." in captured.out