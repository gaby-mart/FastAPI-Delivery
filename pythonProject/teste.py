import requests

#Arquivo para testes em requisições privadas

headers={
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiZXhwIjoxNzgzOTY3MjA4fQ.__UhMzEnx8j0a4_Te5XIyAWD7g06IEa-zKfH0V8oA0c"
}

requisicao = requests.get(" http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())