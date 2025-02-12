import unittest
from datetime import datetime
from main.error import ValidacaoError
from main.domain import Paciente, FilaAtendimento, Risco, Atendimento

class EntitiesTest(unittest.TestCase):

    def test_nome_pessoa_validate(self):

        with self.assertRaises(ValidacaoError) as context:
            Paciente(nome="   ", cpf="11111111111", email="teste@teste.com", nascimento="11/11/1111")
        self.assertIn("nome", context.exception.message)

    def test_criar_paciente_valido(self):
        
        paciente = Paciente(nome="Maria Silva", cpf="22233344455", email="maria@teste.com", nascimento="15/05/1980")
        self.assertEqual(paciente.nome, "Maria Silva")
        self.assertEqual(paciente.cpf, "22233344455")
        self.assertEqual(paciente.email, "maria@teste.com")
        self.assertIsInstance(paciente.nascimento, datetime)




if __name__ == '__main__':
    unittest.main()


