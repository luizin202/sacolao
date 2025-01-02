from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import time

# Configurar Selenium para baixar o PDF (apenas se necessário)
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "./download",  # Mude para o diretório desejado
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Inicializar o Service com o caminho do ChromeDriver
service = Service('./webdriver/chromedriver-win64/chromedriver.exe')

# Inicializar o WebDriver com o Service e as opções configuradas
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Abrir a página desejada
    driver.get('https://www.ceasa.df.gov.br/atacado/')

    # Encontrar o link de download do PDF
    pdf_element = driver.find_element(By.XPATH, '//a[@href="https://www.ceasa.df.gov.br/wp-content/uploads/2024/12/ATACADO-1.pdf"]')
    pdf_url = pdf_element.get_attribute("href")  # Obter o link do atributo href

    # Fazer o download do PDF utilizando requests
    response = requests.get(pdf_url)
    if response.status_code == 200:
        # Salvar o PDF no diretório especificado
        with open("./download/ATACADO-1.pdf", "wb") as file:
            file.write(response.content)
        print("PDF baixado com sucesso!")
    else:
        print(f"Falha ao baixar o PDF. Código de status: {response.status_code}")

    # Opcional: Esperar alguns segundos antes de encerrar
    time.sleep(3)

finally:
    # Fechar o navegador
    driver.quit()
