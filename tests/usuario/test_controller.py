import pytest
from src.controller.usuario.controller import UsuarioController
from src.model.usuario.model import Usuario

def test_login_sucesso(session):
    usuario_controller = UsuarioController(session)
    usuario = usuario_controller.login('admin', 'admin')
    assert usuario is not None

def test_login_falha(session):
    usuario_controller = UsuarioController(session)
    usuario = usuario_controller.login('admin', 'admin')
    assert usuario is None
