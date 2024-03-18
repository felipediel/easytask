# Easytask

Este projeto destina-se a solucionar um desafio de programação de um processo de recrutamento e seleção. Para entender os requisitos da aplicação, acesse o arquivo `REQUIREMENTS.md`.

## Guia de Instalação

Existem várias opções para executar esta aplicação, desde a configuração manual até a utilização de contêineres Docker. Escolha a opção que melhor se adapta às suas necessidades e ambiente.

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

## Acessando o Shell no Contêiner
Ocasionalmente, pode ser necessário acessar o shell diretamente dentro do seu contêiner. Veja como você pode fazer isso:
```bash
$ docker exec -it CONTAINER_ID sh
```

## Criando Migrações
Sempre que você alterar um modelo, você deve criar e aplicar migrações:
```bash
python manage.py db migrate -m "Migração inicial."
python manage.py db upgrade
``` 

Agora que você já sabe instalar e executar a aplicação, vamos ver o que ela pode fazer.

## Endpoints Disponíveis

### Registro de Usuário

- **URL**: `/v1/auth/register`
- **Método HTTP**: `POST`
- **Descrição**: Registra um novo usuário no sistema.
- **Corpo da Requisição (JSON)**:

```json
{
  "name": "Nome do Usuário",
  "email": "exemplo@dominio.com",
  "password": "senha"
}
```

### Login de Usuário

- **URL**: `/v1/auth/login`
- **Método HTTP**: `POST`
- **Descrição**: Autentica um usuário no sistema.
- **Corpo da Requisição (JSON)**:

```json
{
  "email": "exemplo@dominio.com",
  "password": "senha"
}
```

### Logout de Usuário

- **URL**: `/v1/auth/logout`
- **Método HTTP**: `DELETE`
- **Descrição**: Invalida o token de acesso do usuário.
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <access_token>`

### Atualização do Token de Acesso

- **URL**: `/v1/auth/refresh`
- **Método HTTP**: `POST`
- **Descrição**: Gera um novo token de acesso usando um token de atualização.
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <refresh_token>`

### Obtenção da Lista de Tarefas

- **URL**: `/v1/tasks/`
- **Método HTTP**: `GET`
- **Cabeçalho da Requisição**:
  - `Authorization: Bearer <access_token>`
- **Parâmetros de Consulta**:
  - `start` (int): Índice inicial da lista (padrão: 0)
  - `end` (int, opcional): Índice final da lista
  - `limit` (int): Número máximo de resultados a serem retornados (padrão: 5)

## Exemplo de Uso

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
