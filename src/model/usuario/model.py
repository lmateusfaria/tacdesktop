from sqlalchemy import Column, Integer, String, DateTime
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(128), nullable=False)
    data_ultimo_login = Column(DateTime)  # Data do último login
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)  # Data de cadastro
    ip_ultimo_login = Column(String(45))  # IP do último login (IPv4 ou IPv6)
    funcoes_acesso = Column(String(255))  # String para definir funções ou permissões

    def __init__(self, username, senha_hash, funcoes_acesso="usuario"):
        self.username = username
        self.senha_hash = senha_hash
        self.funcoes_acesso = funcoes_acesso
