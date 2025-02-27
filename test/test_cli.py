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
    
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
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
    
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()
    
    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
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

   
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "sim")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        cli.registrar_atendimento()

 
    cli.chamar_proximo()

    captured = capsys.readouterr()
    assert "Próximo Paciente" in captured.out

def test_buscar_historico(capsys):
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)

    
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "João Silva")
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "joao@example.com")
        mp.setattr('builtins.input', lambda _: "01/01/1990")
        cli.registrar_paciente()

    with patch('builtins.input', side_effect=["12345678900", "sim", "não", "não", "não"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        mp.setattr('builtins.input', lambda _: "sim")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        mp.setattr('builtins.input', lambda _: "não")
        cli.registrar_atendimento()

    
    with patch('builtins.input', side_effect=["12345678900"]):
     with pytest.MonkeyPatch.context() as mp:
        mp.setattr('builtins.input', lambda _: "12345678900")
        cli.buscar_historico()

    captured = capsys.readouterr()
    assert "Histórico de atendimentos para João Silva" in captured.out
@pytest.fixture
def setup_cli():
    paciente_repo = PacienteRepository()
    atendimento_repo = AtendimentoRepository(paciente_repo)
    service = ProntoSocorroService(paciente_repo, atendimento_repo)
    cli = TerminalClient(service)
    return cli, paciente_repo, service
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
def test_nome_invalido_caracteres_numericos(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João333Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Nome contém caracteres inválidos." in captured.out
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
def test_cpf_invalido_caracteres_espacos(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "      ", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF deve conter apenas números." in captured.out
def test_registrar_paciente_cpf_duplicado(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/01/1990"]):
        cli.registrar_paciente()
    with patch('builtins.input', side_effect=["Maria Silva", "12345678900", "maria@example.com", "02/02/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "CPF já cadastrado." in captured.out
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
def test_email_invalido_com_arroba_e_nao_formatado(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João@", "12345678900", "joaoexample.com", "01/01/1990"]):
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
def test_email_sem_nome_do_usuario(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "@gmail.com", "01/01/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "E-mail não informado ou contém apenas espaços." in captured.out
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
def test_data_invalida_mes_(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01/dois/1990"]):
        cli.registrar_paciente()
    captured = capsys.readouterr()
    assert "Mês inválido." in captured.out
def test_data_invalida_mes_naoinformado(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["João Silva", "12345678900", "joao@example.com", "01//1990"]):
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
    with patch('builtins.input', return_value="5"):  
        cli.executar()
    captured = capsys.readouterr()
    assert "Saindo do sistema..." in captured.out
def test_executar_opcao_invalida(setup_cli, capsys):
    cli, _, _ = setup_cli
    with patch('builtins.input', side_effect=["6", "5"]):  
        cli.executar()
    captured = capsys.readouterr()
    assert "Opção inválida, tente novamente." in captured.out