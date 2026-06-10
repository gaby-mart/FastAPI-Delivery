from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

#Criando a rota utilizando um decorator
#Dominio/order/lista
@order_router.get("/") #Decorator --> Linha de código feita antes de uma função que atribui uma funcionalidade nova a uma função
async def pedidos():
    return {"Você acessou a rota de pedidos"}