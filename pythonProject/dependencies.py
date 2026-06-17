from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind = db )
        session = Session()
        yield session
    finally:
        session.close()
""" O yield faz a sessão retornar um valor sem encerrar ela"""
"""Try Finally diferentemente do except ele é executado independentemente do resultado do try"""