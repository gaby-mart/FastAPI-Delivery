#Criação das rotas do FastAPI
#Executar no terminal: uvicorn main:app --reload

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") #Chama a chave de segurando do arquivo .env

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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