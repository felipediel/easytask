# Requisitos da Aplicação

Agora, chegou o seu momento de realizar o teste técnico. Confira as orientações.

## O que nós iremos avaliar?

- Separação de contextos;
- Testes e cobertura;
- Tratamento de exceções;
- Manutenabilidade;
- Baixo acoplamento;
- Código pythonico;
- README com todas as instruções de como executar o projeto e como usar os endpoints existentes.

## Requisitos:

- Utilizar algum tipo de autorização na sua API (Ex.: Bearer, Basic Auth).
- Sua API deve consultar os dados utilizando o endpoint [https://jsonplaceholder.typicode.com/todos](https://jsonplaceholder.typicode.com/todos)
- O retorno com sucesso deve ser um JSON no formato:

```json
{
    "id": "id do registro",
    "title": "nome do registro"
}
```

- O retorno com erro deve ser um JSON no formato:

```json
{
    "error": {
        "reason": "descricao do erro"
    }
}
```

- Toda e qualquer consulta na sua API deve gerar um log que deve conter as seguintes informações:
  - timestamp
  - retorno raw da API consultada
  - HTTP status code da API consultada

## Tecnologias:

- Linguagem: Python 3
- Framework: Flask
- Gerenciador de dependências: pipenv ou pip (requirements.txt)
- Você pode usar outras tecnologias/libs que deixem sua implementação flexível, apenas fique atento para o prazo.

## Extras:

Os itens nesta sessão não são obrigatórios, porém contarão como pontos extras:

- Dockerize sua solução, mas não publique sua imagem. Basta criar um diretório docker na raiz do projeto e colocar qualquer arquivo relacionado dentro dele.
- Seguir o 12factor app ([https://12factor.net/pt_br/](https://12factor.net/pt_br/))
- Collection do postman com alguns exemplos de respostas possíveis.
