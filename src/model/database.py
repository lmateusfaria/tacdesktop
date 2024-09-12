from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('postgresql://postgres:postdba@localhost/tac')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()

def get_session():
    """
    Obtém uma nova sessão do banco de dados.
    """
    return SessionLocal()
