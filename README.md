
# FastAPI Upload CSV

Este projeto demonstra como criar uma API usando FastAPI para fazer upload de arquivos CSV e processá-los.

## Funcionalidades

- Upload de arquivos CSV
- Processamento de dados CSV salvando em banco MongoDB ou em mensagem no Rabbit


## Pré-requisitos

- Docker

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/jefersonberg/fastAPI-upload-CSV.git
    cd fastAPI-upload-CSV
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Execute a aplicação FastAPI com o Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

2. Acesse a documentação interativa da API em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

3. Faça upload de um arquivo CSV usando a rota `/api/v1/upload-csv/`.


## Exemplo de Uso

Após iniciar o servidor, você pode usar ferramentas como `curl` ou Postman para enviar um arquivo CSV para a API.

Exemplo de requisição usando `curl`:

```bash
curl -X 'POST'   'http://localhost:8000/api/v1/upload-csv/'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'file=@seu_arquivo.csv'
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
