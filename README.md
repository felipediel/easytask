# Guia de Instalação

## Executando a aplicação

Existem várias opções para executar esta aplicação, desde a configuração manual até a utilização de contêineres Docker. Escolha a opção que melhor se adapta às suas necessidades e ambiente.

### Opção 1: Configuração Manual

1. **Configuração do Banco de Dados**:
   - Configure manualmente um banco de dados PostgreSQL, MySQL ou outro suportado.
   - Ajuste a variável de ambiente `SQLALCHEMY_DATABASE_URI` no arquivo `.env` para a URI do seu banco de dados recém-configurado.

```bash
SQLALCHEMY_DATABASE_URI=your_database_uri
```

2. **Configuração do Ambiente Virtual**:

```bash
$ python3.10 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3. **Aplicação de Migrações**:

```bash
$ flask db upgrade
```

4. **Execução da Aplicação**:

```bash
$ python manage.py run
```

### Opção 2: Construção e Execução de uma Imagem Docker da Aplicação

1. **Configuração do Banco de Dados**:
Configure um banco de dados separadamente e ajuste a variável de ambiente `SQLALCHEMY_DATABASE_URI` no arquivo `.env`.

2. **Construção da Imagem Docker**:

```bash
$ docker build -t easytask .
```

3. **Aplicação de Migrações**:
```bash
$ docker run --env-file .env easytask flask db upgrade
```

4. **Execução da Aplicação**:
```bash
$ docker run --env-file .env easytask python manage.py run
```

### Opção 3: Compor, Construir e Executar a API e o Banco de Dados Juntos
Construa e execute a API e o banco de dados com um único comando:

```bash
$ docker compose up --build
```

## Acessando o shell no contêiner
Ocasionalmente, pode ser necessário acessar o shell diretamente dentro do seu contêiner. Veja como você pode fazer isso:

```bash
$ docker exec -it CONTAINER_ID sh
```

## Criando Migrações
Sempre que você alterar um modelo, você deve criar e aplicar migrações:

```bash
flask db migrate -m "Migração inicial."
flask db upgrade
``` 

Agora que você já sabe executar a aplicação, vamos ver o que ela pode fazer.

# Como usar a API

Este é um guia básico sobre como usar a API.

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
  "password": "senhaDoUsuario"
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
  "password": "senhaDoUsuario"
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
