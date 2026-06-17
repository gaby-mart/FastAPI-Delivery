from pydantic import BaseModel
from typing import Optional

#Cria a tipagem dos paramêtros para a criagem de um usuário

class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True #Criação de uma sub classe do tipo Config que irá conectar com o modelo de bd