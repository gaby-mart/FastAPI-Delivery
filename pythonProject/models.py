#Aqui será criado as classes do banco de dados
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.bd") #Cria e insere o link dos bancos de dados

#Cria a base do banco
Base = declarative_base()

#Criar classes/tabelas
class Usuario(Base):
    __tablename__="usuarios" #Define o nome da tabela no banco de dados

    id = Column("id", Integer, primary_key=True, autoincrement=True) #Column(nome da coluna, tipo de dados, chave primária)
    nome =Column("nome", String)
    email = Column("email", String, nullable=False) #Declara que o campo não pode estar nulo
    senha =Column("senha", String)
    ativo =Column("ativo", Boolean)
    admin =Column("admin", Boolean, default=False) #Sempre que cria um usuário o parametro será falso até a mudança manualmente dele

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__="pedidos"

    #STATUS_PEDIDOS = ( #Tupla (dicionario) feito para a definição dos parametros dos status do pedido
       # ("PENDENTE", "PENDENTE"),
        #("CANCELADO", "CANCELADO"),
        #("FINALIZADO", "FINALIZADO")
    #)


    id =Column("id", Integer, primary_key=True, autoincrement=True)
    status =Column("status", String) #Garante a integridade de seu banco de dados
    usuario =Column("usuario", ForeignKey("usuarios.id"))
    preco =Column("preco", Float)
    itens = relationship("ItemPedido", cascade = "all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)
        
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id =Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#Executar a criação dos metadados do banco