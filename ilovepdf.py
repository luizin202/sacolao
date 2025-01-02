from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Caminho para o seu WebDriver (certifique-se de ter o ChromeDriver instalado)
service = Service('./webdriver/chromedriver-win64/chromedriver.exe')  # Caminho atualizado para o seu chromedriver

# Caminho do arquivo PDF a ser enviado (caminho relativo)
pdf_file_path = './download/ATACADO-1.pdf'

# Converte o caminho relativo para absoluto
pdf_file_path = os.path.abspath(pdf_file_path)

# Caminho de destino para salvar o arquivo baixado
download_folder = os.path.abspath('./download')  # Caminho absoluto para a pasta de download

# Configuração do ChromeOptions para definir o diretório de download
options = webdriver.ChromeOptions()
preferences = {
    "download.default_directory": download_folder,  # Define a pasta de download
    "download.prompt_for_download": False,  # Impede a solicitação de confirmação para o download
    "directory_upgrade": True  # Cria a pasta de download caso ela não exista
}
options.add_experimental_option("prefs", preferences)

# Inicializa o WebDriver com o Service e as opções
driver = webdriver.Chrome(service=service, options=options)

# Acesse o site do ILovePDF
driver.get('https://www.ilovepdf.com/pt/pdf_para_excel')

# Aguarda o carregamento completo da página
time.sleep(3)

# Encontrar e clicar no botão de upload (botão que você mencionou)
upload_button = driver.find_element(By.ID, 'pickfiles')
upload_button.click()

# Aguarda a janela de seleção de arquivos
time.sleep(2)

# Seleciona o arquivo PDF (usando a caixa de diálogo do sistema operacional)
upload_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
upload_input.send_keys(pdf_file_path)

# Aguarda o upload e o processamento do arquivo
time.sleep(5)  # O tempo pode variar dependendo do tamanho do arquivo

# Aguarda até o botão "Converta para EXCEL" estar visível e clicável
convert_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, 'processTaskTextBtn'))
)

# Clica no botão de conversão para Excel
convert_button.click()

# Aguardar o processo de conversão ser finalizado
time.sleep(10)  # Ajuste o tempo conforme necessário



# Aguardar o download ser finalizado
time.sleep(10)  # Ajuste o tempo conforme necessário, dependendo da velocidade de download

# Fecha o navegador
driver.quit()

print("Arquivo PDF convertido para Excel e baixado com sucesso!")
