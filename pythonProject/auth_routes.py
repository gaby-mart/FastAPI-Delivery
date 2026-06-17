from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    #Definir uma docScreen de documentação - Uma descrição da rota para aparecer no fastAPI
    """Todas as rotas do pedido precisam de autentificação"""


    return{"Mensagem": "Você acessou a rota padão de autenticação", "Autentificado" : False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_Schema: UsuarioSchemas, session: Session = Depends(pegar_sessao)): #Session é uma dependencia para criar uma nova sessão do banco de dados
    usuario = session.query(Usuario).filter(Usuario.email==email).all()

    if usuario:
        raise HTTPException(status_code=400, detail="Email do Usuário já cadastrado!") #Indica para o usuário que ele fez alguma coisa errada
    else:
        senha_criptografada = bcrypt_context.hash(usuario_Schema.senha) 
        #Criptografa a senha do usuario'
        novo_usuario = Usuario(usuario_Schema.nome, usuario_Schema.email, senha_criptografada, usuario_Schema.ativo, usuario_Schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_Schema.email}"}
"""Criando uma rota para criar a conta na qual precisa receber o email e a senha na hora de criar o pedido"""