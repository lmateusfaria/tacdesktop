from src.model.usuario.model import Usuario
from src.model.utils import hash_password,verify_password
from src.model.database import get_session
import datetime


def create_user(username, password, funcoes_acesso):
    session = None
    try:
        # Obter uma nova sessão do banco de dados
        session = get_session()

        # Verifica se o usuário já existe
        if session.query(Usuario).filter_by(username=username).first():
            return False  # Usuário já existe

        # Cria novo usuário com os atributos ajustados
        senha_hash = hash_password(password)
        novo_usuario = Usuario(
            username=username,
            senha_hash=senha_hash,
            funcoes_acesso=funcoes_acesso
        )
        
        # Adiciona e confirma a nova entrada no banco
        session.add(novo_usuario)
        session.commit()
        return True

    except Exception as e:
        if session:
            session.rollback()  # O rollback precisa ser chamado no objeto 'session', não 'engine'
        raise e
    finally:
        if session:
            session.close()  # O close também é no objeto 'session', não 'engine'


class LoginController:
    def __init__(self):
        pass  # Não inicializamos a sessão aqui

    def verify_user(self, username, password, ip_login):
        session = get_session()  # Obtém uma nova sessão do banco de dados
        try:
            user = session.query(Usuario).filter_by(username=username).first()

            if user and verify_password(password, user.senha_hash):
                # Atualiza a data e IP do último login
                user.data_ultimo_login = datetime.datetime.utcnow()
                user.ip_ultimo_login = ip_login
                session.commit()

                # Retorna as funções de acesso do usuário
                return True, user.funcoes_acesso
            return False, None
        except Exception as e:
            session.rollback()  # Reverte em caso de erro
            raise e
        finally:
            session.close()  # Fecha a sessão após o uso
