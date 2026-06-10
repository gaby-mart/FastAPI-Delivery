#Criação das rotas do FastAPI
#Executar no terminal: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

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