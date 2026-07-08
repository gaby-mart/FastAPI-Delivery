from fastapi import APIRouter, Depends, HTTPException
from flask import session
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

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

@order_router.get("/listar")
async def listar_pedido( session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException (status_code=401, detail="Você não tem autorização para acessar essa rota.")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }

@order_router.post("/pedido/adicionar/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema : ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario : Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para acessar essa rota.")
    
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido)

    session.add(item_pedido)
    pedido.itens.append(item_pedido)
    pedido.calcular_preco()
    session.commit()

    return{
        "mensagem" : "Item criado com sucesso",
        "item_id" : item_pedido.id, 
        "item_pedido" : pedido.preco
    }