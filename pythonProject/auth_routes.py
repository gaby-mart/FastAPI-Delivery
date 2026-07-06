from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCES_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchemas, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

#Criação dos tokens e validações
def criar_token(id_usuario, duracao_token = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)):
    #Token JWT 

    #Data de espiração do token
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    #Dicionário de informações que irão ser codificadas
    dic_info = {
        "sub": str(id_usuario), 
        "exp": data_expiracao
    }

    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM )
    return jwt_codificado


#Validação do login
def autenticar_usuario(email, senha, session):
     usuario = session.query(Usuario).filter(Usuario.email==email).first()
     if not usuario:
         return False
     elif not bcrypt_context.verify(senha, usuario.senha):
         return False

     return usuario

@auth_router.get("/")
async def home():
    #Definir uma docScreen de documentação - Uma descrição da rota para aparecer no fastAPI
    """Todas as rotas do pedido precisam de autentificação"""


    return{"Mensagem": "Você acessou a rota padão de autenticação", "Autentificado" : False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_Schema: UsuarioSchemas, session: Session = Depends(pegar_sessao), usuario_logado=Depends(verificar_token)): #Session é uma dependencia para criar uma nova sessão do banco de dados
    usuario = session.query(Usuario).filter(Usuario.email==usuario_Schema.email).all()
    
    if usuario:
        raise HTTPException(status_code=400, detail="Email do Usuário já cadastrado!") #Indica para o usuário que ele fez alguma coisa errada
    elif usuario_Schema.admin and not usuario_logado.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para criar usuario admin") #Verifica se usuario é admin
    else:
        senha_criptografada = bcrypt_context.hash(usuario_Schema.senha) 
        #Criptografa a senha do usuario'
        novo_usuario = Usuario(usuario_Schema.nome, usuario_Schema.email, senha_criptografada, usuario_Schema.ativo, usuario_Schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_Schema.email}"}
"""Criando uma rota para criar a conta na qual precisa receber o email e a senha na hora de criar o pedido"""

"""Criação da rota de login com tokens JWT"""

@auth_router.post("/login")
async def login( login_schema : LoginSchema,
    session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        acces_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return{
            "acces_token": acces_token,
            "token_type": "Bearer",
            "refresh_token": refresh_token
            }

@auth_router.post("/login-form")
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(pegar_sessao)
):
    usuario = autenticar_usuario(
        form_data.username,
        form_data.password,
        session
    )
    
    if not usuario:
        # Mudado para 401 (Não autorizado), que é o padrão mais correto para credenciais incorretas
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuário não encontrado ou credenciais inválidas"
        )
    
    # Gerando os tokens
    access_token = criar_token(usuario.id)  # certifique-se de que dura ex: timedelta(minutes=30) dentro da função
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    
    return {
        "access_token": access_token,  # Corrigido a ortografia aqui
        "token_type": "Bearer",
        "refresh_token": refresh_token
    }

#Sistema de criação de um novo Refresh token apartir do login do usuario  
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #verificação do token
    acces_token = criar_token(usuario.id)
    return{
        "acces_token": acces_token,
        "token_type": "Barer"
        }