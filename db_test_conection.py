from db_connection import get_database

def test_connection():
    try:
        # Conectar ao banco de dados
        db = get_database()

        # Verificar as coleções disponíveis
        collections = db.list_collection_names()
        print("Conexão estabelecida com sucesso!")
        print("Coleções disponíveis:", collections)
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", str(e))

# Executar o teste
if __name__ == "__main__":
    test_connection()
