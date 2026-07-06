from fastapi import Depends, HTTPException
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError

def pegar_sessao():
    try:
        Session = sessionmaker(bind = db )
        session = Session()
        yield session
    finally:
        session.close()
""" O yield faz a sessão retornar um valor sem encerrar ela"""
"""Try Finally diferentemente do except ele é executado independentemente do resultado do try"""

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY,algorithms = ALGORITHM) #Da como resposta um dicionário com as informações do usuário
        id_usuario =int(dic_info.get("sub")) #.get quando não encontrado o parâmetro não gera um erro, ele busca coisas dentro do dicionário
        
    except JWTError:
        raise HTTPException(status_code= 401, detail="Acesso Negado, verifique a validade do token")
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    
    return usuario