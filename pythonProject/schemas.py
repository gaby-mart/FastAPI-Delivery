from pydantic import BaseModel
from typing import Optional

#Cria a tipagem dos paramêtros para a criagem de um usuário
#Schema é classe que permite padronizar as informações no banco de dados

class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True #Criação de uma sub classe do tipo Config que irá conectar com o modelo de bd

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float 

    class Config:
        from_attributes = True