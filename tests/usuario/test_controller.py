import pytest
from src.controller.usuario.controller import UsuarioController
from src.model.usuario.model import Usuario

def test_login_sucesso(session):
    usuario_controller = UsuarioController(session)
    usuario = usuario_controller.login('email@teste.com', 'senha_correta')
    assert usuario is not None

def test_login_falha(session):
    usuario_controller = UsuarioController(session)
    usuario = usuario_controller.login('email_incorreto@teste.com', 'senha_errada')
    assert usuario is None
