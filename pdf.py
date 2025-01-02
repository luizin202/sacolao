import pdfplumber
import pandas as pd

# Função para extrair as tabelas do PDF
def extract_table_from_pdf(file_path):
    data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if len(row) >= 5:  # Ajuste o número de colunas conforme necessário
                        data.append(row)
    return data

# Função para salvar os dados em Excel
def save_to_excel(data, output_path):
    df = pd.DataFrame(data, columns=["Produto", "Unidade", "Preço Mínimo", "Preço Comum", "Preço Máximo"])
    df.to_excel(output_path, index=False)
    print(f"Arquivo Excel salvo em {output_path}")

# Caminho do PDF
file_path = "./download/ATACADO-1.pdf"
# Caminho do arquivo Excel de saída
output_path = "./download/saida.xlsx"

# Extrair dados do PDF e salvar em Excel
dados = extract_table_from_pdf(file_path)
save_to_excel(dados, output_path)


