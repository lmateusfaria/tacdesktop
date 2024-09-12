import pytest
from src.model.usuario.model import Usuario
from src.model.utils import hash_password

def test_usuario_creation():
    senha = hash_password('senha123')
    usuario = Usuario(nome="Teste", email="teste@teste.com", senha=senha)
    assert usuario.nome == "Teste"
    assert usuario.email == "teste@teste.com"
    assert usuario.senha != 'senha123'  # Senha deve estar hasheada
