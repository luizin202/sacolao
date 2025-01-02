from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


# Configurar Selenium para baixar o PDF
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": "/download",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(executable_path='/chromedriver/chrome-win64/chrome.exe', options=chrome_options)
driver.get('https://www.ceasa.df.gov.br/atacado/')
link_de_download = driver.find_element(By.XPATH, '//a[@href="https://www.ceasa.df.gov.br/wp-content/uploads/2024/12/ATACADO-1.pdf"]')
link_de_download.click()
time.sleep(10)
driver.quit()



