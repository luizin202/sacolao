import pdfplumber
from pymongo import MongoClient

# Função para extrair dados do PDF
def extract_table_from_pdf(file_path):
    data = []
    start_extraction = False  # Controle para iniciar a extração após encontrar "Acelga"

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            # Extrair as tabelas da página
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Iniciar a extração apenas após encontrar o item "Acelga"
                    if "Acelga" in row:
                        start_extraction = True
                    
                    # Ignorar linhas antes de "Acelga"
                    if not start_extraction:
                        continue

                    # Certifique-se de que a linha tem os dados necessários
                    if len(row) >= 5:
                        produto, unidade, preco_min, preco_comum, preco_max = row[:5]

                        # Tratar valores ausentes ou inválidos
                        produto = produto or "N/A"
                        unidade = unidade or "N/A"
                        preco_min = preco_min or "0"
                        preco_comum = preco_comum or "0"
                        preco_max = preco_max or "0"

                        # Adicionar a linha processada aos dados
                        data.append({
                            "produto": produto.strip(),
                            "unidade": unidade.strip(),
                            "preco_minimo": float(preco_min.replace(",", ".")) if preco_min.replace(",", ".").replace(".", "").isdigit() else None,
                            "preco_comum": float(preco_comum.replace(",", ".")) if preco_comum.replace(",", ".").replace(".", "").isdigit() else None,
                            "preco_maximo": float(preco_max.replace(",", ".")) if preco_max.replace(",", ".").replace(".", "").isdigit() else None
                        })
    return data

# Função para inserir os dados no MongoDB
def insert_data_to_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sacolao"]  # Nome do banco de dados
    collection = db["FLV"]  # Nome da coleção
    collection.insert_many(data)
    print("Dados inseridos com sucesso no MongoDB!")

# Caminho do arquivo PDF
file_path = "./download/ATACADO-1.pdf"

# Extrair e processar os dados
dados = extract_table_from_pdf(file_path)
print(f"Dados extraídos: {dados}")  # Exibir os primeiros itens para validação

# Inserir os dados no MongoDB
insert_data_to_mongodb(dados)
