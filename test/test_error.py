import pytest
from main.error import PSBaseError, ValidacaoError, FilaVaziaError, CPFDuplicadoError, PacienteNaoCadastradoError

# Testes para PSBaseError
def test_psbase_error():
    mensagem = "Erro base do sistema"
    erro = PSBaseError(mensagem)
    assert erro.message == mensagem

# Testes para ValidacaoError
def test_validacao_error():
    mensagem = "Erro de validação"
    erro = ValidacaoError(mensagem)
    assert erro.message == mensagem
    assert isinstance(erro, PSBaseError)  # Verifica se é uma subclasse de PSBaseError

# Testes para FilaVaziaError
def test_fila_vazia_error():
    mensagem = "A fila está vazia"
    erro = FilaVaziaError(mensagem)
    assert erro.message == mensagem
    assert isinstance(erro, PSBaseError)  # Verifica se é uma subclasse de PSBaseError

# Testes para CPFDuplicadoError
def test_cpf_duplicado_error():
    mensagem = "CPF já cadastrado"
    erro = CPFDuplicadoError(mensagem)
    assert erro.message == mensagem
    assert isinstance(erro, PSBaseError)  # Verifica se é uma subclasse de PSBaseError

# Testes para PacienteNaoCadastradoError
def test_paciente_nao_cadastrado_error():
    mensagem = "Paciente não cadastrado"
    erro = PacienteNaoCadastradoError(mensagem)
    assert erro.message == mensagem
    assert isinstance(erro, PSBaseError)  # Verifica se é uma subclasse de PSBaseError

# Testes para verificar o lançamento das exceções
def test_lancamento_psbase_error():
    with pytest.raises(PSBaseError) as exc_info:
        raise PSBaseError("Erro base")
    assert str(exc_info.value) == "Erro base"

def test_lancamento_validacao_error():
    with pytest.raises(ValidacaoError) as exc_info:
        raise ValidacaoError("Erro de validação")
    assert str(exc_info.value) == "Erro de validação"

def test_lancamento_fila_vazia_error():
    with pytest.raises(FilaVaziaError) as exc_info:
        raise FilaVaziaError("Fila vazia")
    assert str(exc_info.value) == "Fila vazia"

def test_lancamento_cpf_duplicado_error():
    with pytest.raises(CPFDuplicadoError) as exc_info:
        raise CPFDuplicadoError("CPF duplicado")
    assert str(exc_info.value) == "CPF duplicado"

def test_lancamento_paciente_nao_cadastrado_error():
    with pytest.raises(PacienteNaoCadastradoError) as exc_info:
        raise PacienteNaoCadastradoError("Paciente não cadastrado")
    assert str(exc_info.value) == "Paciente não cadastrado"