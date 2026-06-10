from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    #Definir uma docScreen de documentação - Uma descrição da rota para aparecer no fastAPI
    """Todas as rotas do pedido precisam de autentificação"""
    return{"Mensagem": "Você acessou a rota padão de autenticação", "Autentificado" : False}

