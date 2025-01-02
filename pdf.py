import pandas as pd
from pymongo import MongoClient

# Caminhos dos arquivos
input_file_path = "./download/ATACADO-1.xlsx"  # Caminho do arquivo Excel original
output_file_path = "./download/saida.xlsx"    # Caminho do arquivo Excel de saída

def extract_table_from_excel(file_path):
    """
    Processa o arquivo Excel e retorna os dados relevantes em um DataFrame,
    iniciando a extração a partir da linha contendo 'Acelga'.
    """
    # Carregar o arquivo Excel sem cabeçalhos para localizar a tabela de interesse
    df = pd.read_excel(file_path, header=None)

    # Detectar a linha onde aparece "Acelga"
    start_index = df[df.apply(lambda row: row.astype(str).str.contains('Acelga', case=False).any(), axis=1)].index.min()

    if start_index is None:
        raise ValueError("A tabela de interesse ('Acelga') não foi encontrada no arquivo.")

    # Recarregar o arquivo com cabeçalhos a partir da linha inicial detectada
    df = pd.read_excel(file_path, header=start_index)

    # Verificar as colunas carregadas
    print("Colunas encontradas no arquivo original:", df.columns.tolist())

    # Renomear colunas para facilitar o uso
    df = df.rename(columns={
        'Acelga': 'produto',
        'Und.  0,7  a  1,2 kg.': 'unidade',
        4: 'preco_minimo',
        5: 'preco_comum',
        6: 'preco_maximo'
    })

    # Garantir que as colunas essenciais existem
    required_columns = ['produto', 'unidade']
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"Colunas obrigatórias ausentes: {required_columns}")

    # Remover linhas inválidas ou vazias
    df = df.dropna(subset=['produto', 'unidade'])

    # Remover linhas duplicadas
    print(f"Linhas antes de remover duplicatas: {len(df)}")
    df = df.drop_duplicates()
    print(f"Linhas após remover duplicatas: {len(df)}")

    # Converter preços para números (float) e arredondar para 2 casas decimais
    for col in ['preco_minimo', 'preco_comum', 'preco_maximo']:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(2)

    # Exibir as primeiras linhas do DataFrame para conferência
    print("Primeiras linhas do DataFrame após processamento:")
    print(df.head())
    print("Número total de registros no DataFrame:", len(df))

    return df

def save_to_excel(df, output_path):
    """
    Salva os dados processados em um arquivo Excel para conferência.
    """
    df.to_excel(output_path, index=False)
    print(f"Dados salvos no arquivo: {output_path}")

def insert_data_to_mongodb(data):
    """
    Insere os dados no banco de dados MongoDB.
    """
    if not data:
        print("Nenhum dado para inserir no MongoDB.")
        return

    print("Inserindo os seguintes dados no MongoDB:")
    print(data[:5])  # Exibe os primeiros 5 registros

    client = MongoClient("mongodb://localhost:27017/")
    db = client["sacolao"]  # Nome do banco de dados
    collection = db["FLV"]  # Nome da coleção
    collection.insert_many(data)
    print("Dados inseridos com sucesso no MongoDB!")

# Extração e processamento
df = extract_table_from_excel(input_file_path)

# Salvar os dados processados em um arquivo Excel para conferência
save_to_excel(df, output_file_path)

# Transformar o DataFrame em uma lista de dicionários e inserir no MongoDB
data = df.to_dict(orient='records')
insert_data_to_mongodb(data)
