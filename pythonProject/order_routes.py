from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

#Criando a rota utilizando um decorator
#Dominio/order/lista
@order_router.get("/") #Decorator --> Linha de código feita antes de uma função que atribui uma funcionalidade nova a uma função
async def pedidos():
    return {"Você acessou a rota de pedidos"}


@order_router.post("/pedidos") #Envia um dado ao bd
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return{"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session:Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    #Validação se usuario é apto para fazer a requisição
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin or usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação.")

    pedido.status = "CANCELADO" 
    session.commit() #Salva a sessão no banco de dados e enecerra o carregamento de dados
    return{
        "mensagem" : f"Pedido número: {pedido.id} cancelado com sucesso", #Quando você chama novamente uma informação do pedido direto do banco de dados você abre o carregamento de dados novamente, possibilitando a visualização novamente
        "pedido" : pedido
    }