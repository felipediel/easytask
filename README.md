# Easytask
[![Python application](https://github.com/felipediel/easytask/actions/workflows/python-app.yaml/badge.svg?branch=master)](https://github.com/felipediel/easytask/actions/workflows/python-app.yaml)
[![codecov](https://codecov.io/gh/felipediel/easytask/graph/badge.svg?token=NIX5W0QEZJ)](https://codecov.io/gh/felipediel/easytask)

Este projeto destina-se a solucionar um desafio de programação de um processo de recrutamento e seleção. Para entender os requisitos da aplicação, acesse o arquivo [REQUIREMENTS.md](REQUIREMENTS.md).

## 1. Guia de Instalação

Existem várias opções para instalar e executar esta aplicação, desde a configuração manual até a utilização de contêineres Docker. Escolha a opção que melhor se adapta às suas necessidades e ambiente.

### Opção 1: Configuração Manual

1. Configure manualmente um banco de dados PostgreSQL, MySQL ou outro suportado. Depois, ajuste a variável de ambiente `SQLALCHEMY_DATABASE_URI` no arquivo `.env` para a URI do seu banco de dados recém-configurado.
```
SQLALCHEMY_DATABASE_URI=your_database_uri
```

2. Configure o ambiente virtual:
```bash
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3. Aplique as migrações:
```bash
$ python manage.py db upgrade
```

4. Execute a aplicação:
```bash
$ python manage.py run
```

### Opção 2: Construção e Execução de uma Imagem Docker da Aplicação

1. Configure um banco de dados separadamente e ajuste a variável de ambiente `SQLALCHEMY_DATABASE_URI` no arquivo `.env` para a URI do seu banco de dados recém-configurado.

2. Construa a imagem Docker:

```bash
$ docker build -t easytask .
```

3. Aplique as migrações:
```bash
$ docker run --env-file .env easytask python manage.py db upgrade
```

4. Execute a aplicação
```bash
$ docker run --env-file .env easytask python manage.py run
```

### Opção 3: Composição e Execução da API e Banco de Dados Juntos
1. Construa e execute a API e o banco de dados com um único comando:
```bash
$ docker compose up --build
```

2. Aplique as migrações:
```bash
$ docker exec CONTAINER_ID python manage.py db upgrade
```

## 2. Acessando o Shell no Contêiner

Ocasionalmente, pode ser necessário acessar o shell diretamente dentro do seu contêiner. Veja como você pode fazer isso:

### Bash
```bash
$ docker exec -it CONTAINER_ID sh
```

### Python shell
```bash
$ docker exec -it CONTAINER_ID python3 manage.py shell
```

## 3. Criando Migrações
Sempre que você alterar um modelo, você deve criar e aplicar migrações:
```bash
python manage.py db migrate -m "Migração inicial."
python manage.py db upgrade
``` 

Agora que você já sabe instalar e executar a aplicação, vamos ver o que ela pode fazer.

## 4. Endpoints Disponíveis

### Registro de Usuário

- **URL**: `/api/v1/auth/register`
- **Método HTTP**: `POST`
- **Descrição**: Registra um novo usuário no sistema.
- **Corpo da Requisição (JSON)**:
```json
{
  "name": "<Nome do usuário>",
  "email": "<E-mail do usuário>",
  "password": "<Senha do usuário>"
}
```
- **Corpo da Resposta (JSON)**:
```json
{
  "id": "<Id do usuário>",
  "name": "<Nome do usuário>",
  "email": "<E-mail do usuário>"
}
```

### Login de Usuário

- **URL**: `/api/v1/auth/login`
- **Método HTTP**: `POST`
- **Descrição**: Autentica um usuário no sistema.
- **Corpo da Requisição (JSON)**:
```json
{
  "email": "<E-mail do usuário>",
  "password": "<Senha do usuário>"
}
```
- **Corpo da Resposta (JSON)**:
```json
{
  "access_token": "<Token de acesso>",
  "refresh_token": "<Token de renovação>"
}
```

### Logout de Usuário

- **URL**: `/api/v1/auth/logout`
- **Método HTTP**: `DELETE`
- **Descrição**: Invalida o token de acesso do usuário.
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <access_token>`
  - ou `Authorization: Bearer <refresh_token>`
- **Corpo da Resposta (JSON)**:
```json
{
  "message": "Access revoked."
}
```

### Atualização do Token de Acesso

- **URL**: `/api/v1/auth/refresh`
- **Método HTTP**: `POST`
- **Descrição**: Gera um novo token de acesso usando um token de atualização.
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <refresh_token>`
- **Corpo da Resposta (JSON)**:
```json
{
  "access_token": "<Token de acesso>"
}
```

### Obtenção da Lista de Tarefas

- **URL**: `/api/v1/tasks/`
- **Método HTTP**: `GET`
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <access_token>`
- **Parâmetros de Consulta**:
  - `start` (int): Índice inicial da lista (padrão: 0)
  - `end` (int, opcional): Índice final da lista
  - `limit` (int): Número máximo de resultados a serem retornados (padrão: 5)
- **Corpo da Resposta (JSON)**:
```json
[
  {
    "id": "<Id da tarefa>",
    "title": "<Título da tarefa>"
  },
  {
    "id": "<Id da tarefa>",
    "title": "<Título da tarefa>"
  },
  {
    "id": "<Id da tarefa>",
    "title": "<Título da tarefa>"
  },
  {
    "id": "<Id da tarefa>",
    "title": "<Título da tarefa>"
  },
  {
    "id": "<Id da tarefa>",
    "title": "<Título da tarefa>"
  },
]
```

## 5. Mensagens de Erro

A seguir estão os status HTTP de erros que podem ser retornados pela aplicação:

- **BAD_REQUEST (400)**: Solicitação inválida.

- **UNAUTHORIZED (401)**: Sem autorização para acessar o recurso.

- **FORBIDDEN (403)**: Acesso proibido ao recurso.

- **NOT_FOUND (404)**: Recurso não encontrado.

- **UNPROCESSABLE_ENTITY (422)**: Recurso em situação improcessável.

- **INTERNAL_SERVER_ERROR (500)**: Erro interno do servidor.

- **SERVICE_UNAVAILABLE (503)**: Serviço temporariamente indisponível.

- **BAD_GATEWAY (502)**: Serviço externo retornou uma resposta inválida ou malformada.

- **GATEWAY_TIMEOUT (504)**: Tempo limite de resposta do serviço externo excedido.

### Formato de Retorno

Todas as mensagens de erro seguem o mesmo formato:

```json
{
    "error": {
        "reason": "<Descrição do erro>"
    }
}
```
Os erros de validação (status HTTP 400) contêm uma chave adicional de contexto para auxiliar na resolução do problema. Eles podem ser classificados em diferentes tipos de erros, dependendo da origem do problema:

- **Erro de Formulário (form_error)**: Indica problemas relacionados aos dados enviados via formulário.
- **Erro no Corpo da Requisição (body_error)**: Refere-se a erros identificados no corpo da requisição.
- **Erro no Caminho do Recurso (path_error)**: Sinaliza problemas relacionados ao caminho do recurso requisitado.
- **Erro nos Parâmetros de Consulta (query_error)**: Indica erros encontrados nos parâmetros de consulta da requisição.

Aqui está um exemplo do formato de retorno com o contexto:

```json
{
    "error": {
        "reason": "Erro de validação",
        "context": {
            "body_params": [
                {
                    "type": "value_error",
                    "loc": ["email"],
                    "msg": "E-mail já existe",
                    "input": "john@doe.com"
                }
            ]
        }
    }
}
```

Neste exemplo, o erro específico é indicado como um erro no corpo da requisição (body_error), e detalhes adicionais são fornecidos no contexto (context), como o tipo de erro (type), o local onde ocorreu (loc), a mensagem de erro (msg) e o valor de entrada que causou o erro (input).

## 6. Exemplo de Uso

Aqui está um exemplo de como usar a API com o Python usando a biblioteca `requests`:

```python
import requests

# URL base da API
base_url = "http://localhost:5000"

# Dados para registro de usuário
register_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "supersecret"
}

# Dados para login de usuário
login_data = {
    "email": "john.doe@example.com",
    "password": "supersecret"
}

# Registrar usuário
register_response = requests.post(f"{base_url}/v1/auth/register", json=register_data)
print(register_response.json())

# Fazer login
login_response = requests.post(f"{base_url}/v1/auth/login", json=login_data)
print(login_response.json())

# Extrair o token de acesso
access_token = login_response.json()["access_token"]

# Usar o token de acesso para obter a lista de tarefas
headers = {"Authorization": f"Bearer {access_token}"}
tasks_response = requests.get(f"{base_url}/v1/tasks", headers=headers)
print(tasks_response.json())

# Fazer logout
logout_response = requests.delete(f"{base_url}/v1/auth/logout", headers=headers)
print(logout_response.json())
```

Lembre-se de substituir `"http://localhost:5000"` com a URL real da sua API.
