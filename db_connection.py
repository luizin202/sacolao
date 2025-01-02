from pymongo import MongoClient

def get_database():
    """
    Função para conectar ao MongoDB e retornar o objeto do banco de dados.
    """
    # URL de conexão com o MongoDB
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Nome do banco de dados
    DB_NAME = "sacolao"

    # Criar a conexão com o MongoDB
    client = MongoClient(CONNECTION_STRING)

    # Retornar o banco de dados
    return client[DB_NAME]