#Criação das rotas do FastAPI
#Executar no terminal: uvicorn main:app --reload

from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") #Chama a chave de segurando do arquivo .env
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))
"""Variaveis de ambiente sempre originalemnte são criadas como str, para que elas possam ser utilizadas para
fazer contas temos que mudar a tipagem para INT ou FLOAT"""

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
#Rest APIs
# Get --> Ler/pegas
# Post --> enviar/criar
# Put/Patch --> edição
# Delete --> deletar

#endpoint: xxxxx/ordens (path)
#As rotes são recomendadas serem criadas em um arquivo a parte